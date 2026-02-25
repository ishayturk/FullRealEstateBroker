# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Exam Engine | PDF + Gemini question extraction
import streamlit as st
import os, json, random, base64, re, time
import google.generativeai as genai
import pdfplumber

EXAMS_DIR = "exams_data"
GEMINI_MODEL = "gemini-1.5-flash"

# --- SECTION: GEMINI SETUP ---
def get_gemini_model():
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(GEMINI_MODEL)

# --- SECTION: EXAM FILE SELECTION ---
def get_exam_files():
    """מחזיר רשימת זוגות (test, ans) מהתיקייה"""
    if not os.path.exists(EXAMS_DIR):
        return []
    files = os.listdir(EXAMS_DIR)
    test_files = sorted([f for f in files if f.startswith("test_") and f.endswith(".pdf")])
    pairs = []
    for tf in test_files:
        # test_feb_1_2025.pdf → ans_feb_1_2025.pdf
        ans_name = tf.replace("test_", "ans_", 1)
        ans_path = os.path.join(EXAMS_DIR, ans_name)
        test_path = os.path.join(EXAMS_DIR, tf)
        if os.path.exists(ans_path):
            pairs.append((test_path, ans_path))
    return pairs

def pick_random_exam():
    """בוחר בחינה אקראית שלא נבחרה בסשן הנוכחי"""
    pairs = get_exam_files()
    if not pairs:
        return None, None
    used = st.session_state.get("used_exams", set())
    available = [p for p in pairs if p[0] not in used]
    if not available:
        # אם כולן נוצלו — מאפס
        available = pairs
        st.session_state.used_exams = set()
    chosen = random.choice(available)
    st.session_state.used_exams = used | {chosen[0]}
    return chosen

# --- SECTION: ANSWER KEY PARSING ---
def parse_answer_key(ans_path):
    """קורא קובץ תשובות ומחזיר dict: {1: 'ג', 2: 'ד', ...}"""
    label_map = {'א': 'א', 'ב': 'ב', 'ג': 'ג', 'ד': 'ד',
                 'a': 'א', 'b': 'ב', 'c': 'ג', 'd': 'ד',
                 'A': 'א', 'B': 'ב', 'C': 'ג', 'D': 'ד'}
    answers = {}
    try:
        with pdfplumber.open(ans_path) as pdf:
            text = pdf.pages[0].extract_text() or ""
        # הטקסט הפוך — מחפשים תבנית של מספר ותשובה
        # תבנית: )ג( 1 או )א,ב,ג,ד( 9
        # כולל כל התשובות
        all_pattern = re.findall(r'\)([דגבא,]+)\(\s+(\d+)', text)
        for ans_str, q_num in all_pattern:
            q = int(q_num)
            if ',' in ans_str:
                answers[q] = "הכל"
            else:
                answers[q] = ans_str
    except Exception as e:
        pass
    return answers

# --- SECTION: QUESTION EXTRACTION VIA GEMINI ---
def extract_question_from_pdf(test_path, question_number):
    """שולח את ה-PDF ל-Gemini ומבקש שאלה ספציפית"""
    try:
        with open(test_path, "rb") as f:
            pdf_bytes = f.read()
        pdf_b64 = base64.b64encode(pdf_bytes).decode()

        prompt = f"""קרא את שאלון הבחינה המצורף בעברית.
חלץ את שאלה מספר {question_number} בלבד.
החזר JSON בדיוק בפורמט הבא ללא שום טקסט נוסף:
{{
  "number": {question_number},
  "text": "טקסט השאלה המלא",
  "options": {{
    "א": "טקסט תשובה א",
    "ב": "טקסט תשובה ב",
    "ג": "טקסט תשובה ג",
    "ד": "טקסט תשובה ד"
  }}
}}
חשוב: החזר רק JSON תקין, ללא markdown, ללא הסברים."""

        model = get_gemini_model()
        response = model.generate_content([
            {"mime_type": "application/pdf", "data": pdf_b64},
            prompt
        ])
        raw = response.text.strip()
        # נקה markdown אם יש
        raw = re.sub(r'^```[a-z]*\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)
        data = json.loads(raw)
        return data
    except Exception as e:
        return None

# --- SECTION: STATE INITIALIZATION ---
def initialize_exam_state():
    defaults = {
        "step": "instructions",
        "current_q": 1,
        "exam_questions": {},      # {1: {...}, 2: {...}, ...} שאלות שנטענו
        "answer_key": {},          # {1: 'ג', 2: 'ד', ...}
        "user_answers": {},        # {1: 'ב', ...} תשובות משתמש
        "nav_active_questions": set(),
        "finish_button_visible": False,
        "exam_start_time": None,
        "test_path": None,
        "ans_path": None,
        "used_exams": set(),
        "q1_ready": False,         # האם שאלה 1 מוכנה
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- SECTION: QUESTION MANAGEMENT ---
def ensure_question_exists(n):
    """מוודא שהשאלה קיימת — אם לא, טוען אותה"""
    if n < 1 or n > 25:
        return
    if n in st.session_state.exam_questions:
        return
    if not st.session_state.test_path:
        return
    q_data = extract_question_from_pdf(st.session_state.test_path, n)
    if q_data:
        correct = st.session_state.answer_key.get(n, "")
        st.session_state.exam_questions[n] = {
            "number": n,
            "text": q_data.get("text", ""),
            "options": q_data.get("options", {}),
            "correct_label": correct,
            "correct_text": q_data.get("options", {}).get(correct, ""),
            "allow_all": correct == "הכל",
        }
        if n == 1:
            st.session_state.q1_ready = True

def load_exam():
    """טוען בחינה חדשה — בוחר קבצים ומפרסר תשובות"""
    test_path, ans_path = pick_random_exam()
    if not test_path:
        return False
    st.session_state.test_path = test_path
    st.session_state.ans_path = ans_path
    st.session_state.answer_key = parse_answer_key(ans_path)
    st.session_state.exam_questions = {}
    st.session_state.user_answers = {}
    st.session_state.nav_active_questions = set()
    st.session_state.q1_ready = False
    st.session_state.finish_button_visible = False
    st.session_state.exam_start_time = None
    return True

# --- SECTION: USER ANSWER RECORDING ---
def record_answer(q_num, label):
    """רושם תשובת משתמש ומחשב ניקוד"""
    st.session_state.user_answers[q_num] = {
        "label": label,
        "text": st.session_state.exam_questions.get(q_num, {}).get("options", {}).get(label, ""),
    }

def get_points(q_num):
    """מחזיר 4 אם ענה נכון, 0 אם לא"""
    q = st.session_state.exam_questions.get(q_num)
    if not q:
        return 0
    user = st.session_state.user_answers.get(q_num, {})
    user_label = user.get("label", "")
    correct = q.get("correct_label", "")
    if q.get("allow_all"):
        return 4 if user_label else 0
    return 4 if user_label == correct else 0

def get_total_score():
    total = 0
    for q_num in range(1, 26):
        total += get_points(q_num)
    return total

# --- SECTION: TIMER ---
def get_remaining_seconds():
    if not st.session_state.exam_start_time:
        return 90 * 60
    elapsed = time.time() - st.session_state.exam_start_time
    return max(0, int(90 * 60 - elapsed))

# --- SECTION: EXAM DATA COMPATIBILITY (legacy) ---
# שמירת תאימות עם main.py הקיים
@property
def exam_data_compat():
    return {k: {
        "question": v["text"],
        "options": list(v["options"].values()),
        "correct": v["correct_label"],
    } for k, v in st.session_state.exam_questions.items()}
# סוף קובץ
