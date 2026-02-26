# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Exam Engine | JSON-based
import streamlit as st
import os, json, random, time

EXAMS_DIR = "exams_data"

# --- SECTION: EXAM FILE SELECTION ---
def get_exam_files():
    if not os.path.exists(EXAMS_DIR):
        return []
    return [os.path.join(EXAMS_DIR, f) for f in os.listdir(EXAMS_DIR) if f.endswith(".json")]

def pick_random_exam():
    files = get_exam_files()
    if not files:
        return None
    used = st.session_state.get("used_exams", set())
    available = [f for f in files if f not in used]
    if not available:
        available = files
        st.session_state.used_exams = set()
    chosen = random.choice(available)
    st.session_state.used_exams = used | {chosen}
    return chosen

# --- SECTION: STATE INITIALIZATION ---
def initialize_exam_state():
    defaults = {
        "step": "instructions",
        "current_q": 1,
        "exam_questions": {},
        "user_answers": {},
        "nav_active_questions": set(),
        "finish_button_visible": False,
        "exam_start_time": None,
        "exam_file": None,
        "used_exams": set(),
        "q1_ready": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- SECTION: LOAD EXAM ---
def load_exam():
    exam_file = pick_random_exam()
    if not exam_file:
        return False
    with open(exam_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    st.session_state.exam_file = exam_file
    st.session_state._exam_raw = data
    st.session_state.exam_questions = {}
    st.session_state.user_answers = {}
    st.session_state.nav_active_questions = set()
    st.session_state.finish_button_visible = False
    st.session_state.exam_start_time = None
    # טעינת שאלה 1 מיידית
    q1 = data.get("questions", {}).get("1")
    if q1:
        st.session_state.exam_questions[1] = q1
        st.session_state.q1_ready = True
    else:
        st.session_state.q1_ready = False
    return True

# --- SECTION: QUESTION MANAGEMENT ---
def ensure_question_exists(n):
    if n < 1 or n > 25:
        return
    if n in st.session_state.exam_questions:
        return
    raw = st.session_state.get("_exam_raw", {})
    q = raw.get("questions", {}).get(str(n))
    if q:
        st.session_state.exam_questions[n] = q
        if n == 1:
            st.session_state.q1_ready = True

# --- SECTION: USER ANSWER RECORDING ---
def record_answer(q_num, label):
    st.session_state.user_answers[q_num] = {
        "label": label,
        "text": st.session_state.exam_questions.get(q_num, {}).get("options", {}).get(label, ""),
    }

def get_points(q_num):
    q = st.session_state.exam_questions.get(q_num)
    if not q:
        return 0
    user_label = st.session_state.user_answers.get(q_num, {}).get("label", "")
    correct = q.get("correct_label", "")
    return 4 if user_label == correct else 0

def get_total_score():
    return sum(get_points(n) for n in range(1, 26))

# --- SECTION: TIMER ---
def get_remaining_seconds():
    if not st.session_state.exam_start_time:
        return 90 * 60
    elapsed = time.time() - st.session_state.exam_start_time
    return max(0, int(90 * 60 - elapsed))
# סוף קובץ
