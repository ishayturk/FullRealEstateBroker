# ==========================================
# Project: מתווך בקליק | Version: 1217-G2
# ==========================================
import streamlit as st
import google.generativeai as genai
import json, re

st.set_page_config(page_title="מתווך בקליק", layout="wide")
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { 
        width: 100%; border-radius: 8px; font-weight: bold; height: 3em; 
    }
    .top-link { 
        display: inline-block; width: 100%; text-align: center; 
        border-radius: 8px; text-decoration: none; border: 1px solid #d1d5db;
        font-weight: bold; height: 2.8em; line-height: 2.8em;
        background-color: transparent; color: inherit;
    }
    .v-footer {
        text-align: center; color: rgba(255, 255, 255, 0.1);
        font-size: 0.7em; margin-top: 50px; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

SYLLABUS = {
    "חוק המתווכים": ["רישוי והגבלות", "הגינות וזהירות", "הזמנה"],
    "תקנות המתווכים": ["פרטי הזמנה 1997", "פעולות שיווק 2004", "דמי תיווך"],
    "חוק המקרקעין": ["בעלות וזכויות", "בתים משותפים", "הערות אזהרה"],
    "חוק המכר (דירות)": ["מפרט וגילוי", "בדק ואחריות", "הבטחת השקעות"],
    "חוק החוזים": ["כריתת חוזה", "פגמים בחוזה", "תרופות והפרה"],
    "חוק התכנון והבנייה": ["היתרים", "היטל השבחה", "תוכניות מתאר"],
    "חוק מיסוי מקרקעין": ["מס שבח", "מס רכישה", "שווי שוק"],
    "חוק הגנת הצרכן": ["ביטול עסקה", "הטעיה בפרסום"],
    "דיני ירושה": ["סדר הירושה", "צוואות"],
    "חוק העונשין": ["עבירות מרמה וזיוף"]
}

def fetch_q_ai(topic):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        p = f"צור שאלה אמריקאית על {topic} למבחן המתווכים."
        p += " החזר אך ורק JSON תקני במבנה הבא:"
        p += " {'q':'','options':['','','',''],'correct':'','explain':''}"
        res = m.generate_content(p).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match: 
            return json.loads(match.group().replace("'", '"'))
    except: return None
    return None

def stream_ai_lesson(p):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        full_p = p + " כתוב שיעור הכנה מעמיק למבחן המתווכים. ללא כותרות."
        response = m.generate_content(full_p, stream=True)
        placeholder = st.empty()
        txt = ""
        for chunk in response:
            txt += chunk.text
            placeholder.markdown(txt + "▌")
        placeholder.markdown(txt)
        return txt
    except: 
        return "⚠️ תקלה בטעינה."

if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "q_count": 0, "quiz_active": False, 
        "show_ans": False, "lesson_txt": "", "q_data": None, 
        "correct_answers": 0, "quiz_finished": False
    })

st.title("🏠 מתווך בקליק")

if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.update({"user": u, "step": "menu"})
        st.rerun()

elif st.session_state.step == "menu":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים"):
            st.session_state.step = "study"; st.rerun()
    with c2:
        if st.button("⏱️ גש/י למבחן"): st.info("בקרוב!")

elif st.session_state.step == "study":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    sel = st.selectbox("בחר נושא:", ["בחר נושא"] + list(SYLLABUS.keys()))
    if sel != "בחר נושא" and st.button("טען נושא"):
        st.session_state.update({
            "selected_topic": sel, "step": "lesson_run", "quiz_active": False, 
            "lesson_txt": "", "q_data": None, "q_count": 0, 
            "correct
