# ==========================================
# Project: מתווך בקליק | Version: 1213-C-01
# ==========================================
import streamlit as st
import google.generativeai as genai
import json, re

st.set_page_config(page_title="מתווך בקליק", layout="wide")
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    .top-link { 
        display: inline-block; width: 100%; text-align: center; 
        border-radius: 8px; text-decoration: none; border: 1px solid #d1d5db;
        font-weight: bold; height: 2.8em; line-height: 2.8em;
    }
    .v-footer { text-align: center; color: rgba(255, 255, 255, 0.1); font-size: 0.7em; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

SYLLABUS = {
    "חוק המתווכים": ["רישוי והגבלות", "הגינות וזהירות", "הזמנה ובלעדיות", "פעולות שאינן תיווך"],
    "תקנות המתווכים": ["פרטי הזמנה 1997", "פעולות שיווק 2004", "דמי תיווך"],
    "חוק המקרקעין": ["בעלות וזכויות", "בתים משותפים", "עסקאות נוגדות", "הערות אזהרה", "שכירות וזיקה"],
    "חוק המכר (דירות)": ["מפרט וגילוי", "בדק ואחריות", "איחור במסירה", "הבטחת השקעות"],
    "חוק החוזים": ["כריתת חוזה", "פגמים בחוזה", "תרופות והפרה", "ביטול והשבה"],
    "חוק התכנון והבנייה": ["היתרים ושימוש חורג", "היטל השבחה", "תוכניות מתאר", "מוסדות התכנון"],
    "חוק מיסוי מקרקעין": ["מס שבח", "מס רכישה", "הקלות לדירת מגורים", "שווי שוק"],
    "חוק הגנת הצרכן": ["ביטול עסקה", "הטעיה בפרסום"],
    "דיני ירושה": ["סדר הירושה", "צוואות"],
    "חוק העונשין": ["עבירות מרמה וזיוף"]
}

def fetch_q_ai(topic, is_exam=False):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        level = "קשה מאוד" if is_exam else "קשה"
        p = f"צור שאלה אמריקאית {level} על {topic}. החזר JSON תקני בלבד: {{'q':'','options':['','','',''],'correct':'','explain':''}}"
        res = m.generate_content(p).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match: return json.loads(match.group())
    except: return None

def stream_ai_lesson(p):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        full_p = p + " כתוב שיעור הכנה מעמיק. פרט סעיפי חוק ודוגמאות. ללא כותרות."
        response = m.generate_content(full_p, stream=True)
        placeholder = st.empty()
        full_text = ""
        for chunk in response:
            full_text += chunk.text
            placeholder.markdown(full_text + "▌")
        placeholder.markdown(full_text)
        return full_text
    except: return "⚠️ תקלה."

# אתחול
if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "q_count": 0, "quiz_active": False,
        "show_ans": False, "lesson_txt": "", "q_data": None, "correct_answers": 0,
        "quiz_finished": False, "completed_exams": [], "ex_data": None,
        "ex_count": 0, "ex_score": 0, "ex_show_ans": False
    })

st.title("🏠 מתווך בקליק")

if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.update({"user": u, "step": "menu"}); st.rerun()

elif st.session_state.step == "menu":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    if c1.button("📚 לימוד לפי נושאים"):
        st.session_state.step = "study"; st.rerun()
    if c2.button("⏱️ גש/י למבחן"):
        # מציאת נושא שטרם נבחן עליו
        available = [k for k in SYLLABUS.keys() if k not in st.session_state.completed_exams]
        if not available: st.session_state.completed_exams = [] # איפוס אם הכל הושלם
        st.session_state.ex_topic = available[0] if available else list(SYLLABUS.keys())[0]
        st.session_state.step = "exam"; st.rerun()

elif st.session_state.step == "exam":
    st.header(f"⏱️ מבחן בנושא: {st.session_state.ex_topic}")
    
    if st.session_state.ex_count == 0:
        if st.button("התחל מבחן (25 שאלות)"):
            st.session_state.ex_count = 1; st.session_state.ex_score = 0
            st.session_state.ex_data = fetch_q_ai(st.session_state.ex_topic, True)
            st.rerun()
    elif st.session_state.ex_count <= 25:
        q = st.session_state.ex_data
        st.subheader(f"שאלה {st.session_state.ex_count} מתוך 25")
        if q:
            ans = st.radio(q['q'], q['options'], index=None, key=f"ex_{st.session_state.ex_count}")
            if st.button("אשר תשובה ועבור לשאלה הבאה"):
                if ans == q['correct']: st.session_state.ex_score += 1
                if st.session_state.ex_count < 25:
                    st.session_state.ex_data = fetch_q_ai(st.session_state.ex_topic, True)
                    st.session_state.ex_count += 1
                else:
                    st.session_state.ex_count = 26 # סיום
                st.rerun()
    else:
        st.success(f"המבחן הסתיים! ציון: {int((st.session_state.ex_score/25)*100)}")
        st.session_state.completed_exams.append(st.session_state.ex_topic)
        if st.button("חזרה לתפריט"):
            st.session_state.update({"step": "menu", "ex_count": 0, "ex_data": None}); st.rerun()

elif st.session_state.step == "study":
    sel = st.selectbox("בחר נושא:", ["בחר..."] + list(SYLLABUS.keys()))
    if sel != "בחר..." and st.button("טען נושא"):
        st.session_state.update({"selected_topic": sel, "step": "lesson_run", "quiz_active": False, "lesson_txt": "", "q_count": 0})
        st.rerun()

elif st.session_state.step == "lesson_run":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    subs = SYLLABUS.get(topic, [])
    cols = st.columns(len(subs))
    for i, s in enumerate(subs):
        if cols[i].button(s, key=f"sub_{i}"):
            st.session_state.update({"current_sub": s, "lesson_txt": "LOADING", "quiz_active": False})
            st.rerun()

    if st.session_state.get("lesson_txt") == "LOADING":
        st.session_state.lesson_txt = stream_ai_lesson(f"שיעור על {st.session_state.current_sub}")
        st.rerun()
    elif st.session_state.get("lesson_txt"):
        st.markdown(st.session_state.lesson_txt)

    if st.session_state.quiz_active and st.session_state.q_data:
        q = st.session_state.q_data
        st.subheader(f"📝 שאלה {st.session_state.q_count}/10")
        ans = st.radio(q['q'], q['options'], index=None, key=f"q_{st.session_state.q_count}")
        if st.session_state.show_ans:
            if ans == q['correct']: st.success("נכון!")
            else: st.error(f"טעות. הנכון: {q['correct']}")

    st.write("")
    f_cols = st.columns([2.5, 2, 1.5, 3])
    with f_cols[0]:
        if (st.session_state.get("selected_topic") or st.session_state.lesson_txt != "") and not st.session_state.quiz_finished:
            if not st.session_state.quiz_active:
                if st.button("📝 שאלון לבחינה עצמית"):
                    res = fetch_q_ai(topic)
                    if res: st.session_state.update({"q_data": res, "q_count": 1, "quiz_active": True, "show_ans": False})
                    st.rerun()
            elif not st.session_state.show_ans:
                if st.button("✅ בדוק"):
                    if st.session_state.get(f"q_{st.session_state.q_count}") == st.session_state.q_data['correct']:
                        st.session_state.correct_answers += 1
                    st.session_state.show_ans = True; st.rerun()
            elif st.session_state.q_count < 10:
                if st.button("➡️ הבא"):
                    res = fetch_q_ai(topic)
                    st.session_state.update({"q_data": res, "q_count": st.session_state.q_count + 1, "show_ans": False}); st.rerun()

    if f_cols[1].button("🏠 תפריט"):
        st.session_state.step = "menu"; st.rerun()
