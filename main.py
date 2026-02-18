# ==========================================
# Project: מתווך בקליק | Version: 1218-G3
# ==========================================
import streamlit as st
import google.generativeai as genai
import json, re, time

st.set_page_config(page_title="מתווך בקליק", layout="wide")
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

# עיצוב CSS בשורות קצרות
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { 
        width: 100%; border-radius: 8px; 
        font-weight: bold; height: 3em; 
    }
    .top-link { 
        display: inline-block; width: 100%; text-align: center; 
        border-radius: 8px; text-decoration: none; 
        border: 1px solid #d1d5db; font-weight: bold; 
        height: 2.8em; line-height: 2.8em;
    }
</style>
""", unsafe_allow_html=True)

# סילבוס במבנה אנכי למניעת שורות ארוכות
SYLLABUS = {
    "חוק המתווכים": [
        "רישוי והגבלות", "הגינות וזהירות", 
        "הזמנה ובלעדיות", "פעולות שאינן תיווך"
    ],
    "תקנות המתווכים": [
        "פרטי הזמנה 1997", "פעולות שיווק 2004", "דמי תיווך"
    ],
    "חוק המקרקעין": [
        "בעלות וזכויות", "בתים משותפים", "עסקאות נוגדות", 
        "הערות אזהרה", "שכירות וזיקה"
    ],
    "חוק המכר (דירות)": [
        "מפרט וגילוי", "בדק ואחריות", 
        "איחור במסירה", "הבטחת השקעות"
    ],
    "חוק החוזים": [
        "כריתת חוזה", "פגמים בחוזה", 
        "תרופות והפרה", "ביטול והשבה"
    ],
    "חוק התכנון והבנייה": [
        "היתרים ושימוש חורג", "היטל השבחה", 
        "תוכניות מתאר", "מוסדות התכנון"
    ],
    "חוק מיסוי מקרקעין": [
        "מס שבח (חישוב ופטורים)", "מס רכישה", 
        "הקלות לדירת מגורים", "שווי שוק"
    ],
    "חוק הגנת הצרכן": ["ביטול עסקה", "הטעיה בפרסום"],
    "דיני ירושה": ["סדר הירושה", "צוואות"],
    "חוק העונשין": ["עבירות מרמה וזיוף"]
}

def fetch_q_ai(topic):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        p = f"צור שאלה אמריקאית קשה על {topic}. החזר JSON תקני בלבד."
        res = m.generate_content(p).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match: return json.loads(match.group())
    except: return None

def stream_ai_lesson(p):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        response = m.generate_content(p, stream=True)
        placeholder = st.empty()
        full_text = ""
        for chunk in response:
            full_text += chunk.text
            placeholder.markdown(full_text + "▌")
        placeholder.markdown(full_text)
        return full_text
    except: return "⚠️ תקלה."

# אתחול במבנה קריא
if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "q_count": 0, 
        "quiz_active": False, "show_ans": False, 
        "lesson_txt": "", "q_data": None, 
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
    if c1.button("📚 לימוד לפי נושאים"):
        st.session_state.step = "study"
        st.rerun()
    if c2.button("⏱️ גש/י למבחן"):
        st.info("בקרוב!")

elif st.session_state.step == "study":
    sel = st.selectbox("בחר נושא:", ["בחר..."] + list(SYLLABUS.keys()))
    if sel != "בחר..." and st.button("טען נושא"):
        st.session_state.update({
            "selected_topic": sel, "step": "lesson_run", 
            "quiz_active": False, "lesson_txt": "", 
            "q_data": None, "q_count": 0, 
            "correct_answers": 0, "quiz_finished": False
        })
        st.rerun()
    if st.button("🏠 חזרה לתפריט"):
        st.session_state.step = "menu"
        st.rerun()

elif st.session_state.step == "lesson_run":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    subs = SYLLABUS.get(topic, [])
    sub_cols = st.columns(len(subs))
    for i, s in enumerate(subs):
        if sub_cols[i].button(s, key=f"sub_{i}"):
            st.session_state.update({
                "current_sub": s, "lesson_txt": "LOADING", 
                "quiz_active": False, "q_data": None, 
                "quiz_finished": False, "q_count": 0, "correct_answers": 0
            })
            st.rerun()
