# ==========================================
# Project: מתווך בקליק | Version: 1239-G2
# ==========================================
import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide")

st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    .timer-box {
        position: fixed; top: 10px; left: 10px; background: #ff4b4b; color: white;
        padding: 8px; border-radius: 8px; z-index: 1000; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏠 מתווך בקליק")

if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login",
        "exam_qs": [], "current_q_idx": 0, "max_reached_idx": 0,
        "exam_answers": {}, "start_time": None, "lesson_txt": "", "current_sub": None
    })

if st.session_state.user:
    st.markdown(f"### **שלום, {st.session_state.user}**")

# מאגר נושאים ותתי-נושאים (ללא המילה סילבוס)
TOPICS_DATA = {
    "חוק המתווכים": ["רישוי והגבלות", "הגינות וזהירות", "הזמנה בכתב", "בלעדיות", "פעולות שיווק", "איסור פעולות משפטיות"],
    "חוק המקרקעין": ["בעלות וזכויות", "בתים משותפים", "הערות אזהרה", "עסקאות ורישום", "זכויות במקרקעין", "פירוק שיתוף"],
    "חוק החוזים": ["כריתת חוזה", "פגמים בחוזה", "תרופות בשל הפרה", "ביטול חוזה", "תום לב"],
    "חוק התכנון והבנייה": ["מוסדות תכנון", "היתרים", "שימוש חורג", "היטל השבחה", "תמ״א 38", "תכנית מתאר"],
    "חוק הגנת הצרכן": ["הטעיה וניצול מצוקה", "ביטול עסקה", "מכירה באשראי"],
    "חוק מיסוי מקרקעין": ["מס שבח", "מס רכישה", "פטורים", "שווי שוק"],
    "חוק הגנת הדייר": ["דיירות מוגנת", "דמי מפתח", "עילות פינוי"],
    "חוק המכר": ["חוק המכר (דירות)", "הבטחת השקעות", "פיצוי על איחור"]
}

TEST_EXAM = [{"q": f"שאלה לבדיקה {i+1}", "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"], "correct_idx": 0} for i in range(25)]

def stream_ai_lesson(p):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        res = m.generate_content(p, stream=True)
        ph = st.empty(); txt = ""
        for chunk in res:
            txt += chunk.text
            ph.markdown(txt + "▌")
        ph.markdown(txt)
        return txt
    except: return "⚠️ תקלה בחיבור ל-AI."

if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.user = u
        st.session_state.step = "menu"; st.rerun()

elif st.session_state.step == "menu":
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים"): st.session_state.step = "study"; st.rerun()
    with c2:
        if st.button("⏱️ גש למבחן מלא (3 דק')"):
            st.session_state.update({
                "step": "exam_run", "start_time": time.time(),
                "exam_qs": TEST_EXAM[:5], "exam_answers": {}, 
                "current_q_idx": 0, "max_reached_idx": 0
            })
            st.rerun()

elif st.session_state.step == "study":
    sel = st.selectbox("בחר נושא לימוד:", ["בחר נושא"] + list(TOPICS_DATA.keys()))
    if sel != "בחר נושא":
        subs = TOPICS_DATA[sel]
        cols = st.columns(len(subs))
        for i, s in enumerate(subs):
            if cols[i].button(s):
                st.session_state.current_sub = s
                st.session_state.step = "lesson_run"
                st.session_state.lesson_txt = "LOADING"; st.rerun()
    if st.button("🏠 חזרה לתפריט ראשי"): st.session_state.step = "menu"; st.rerun()

elif st.session_state.step == "lesson_run":
    st.subheader(f"📖 שיעור בנושא: {st.session_state.current_sub}")
    if st.session_state.lesson_txt == "LOADING":
        st.session_state.lesson_txt = stream_ai_lesson(f"הסבר מקצועי למתווכים על: {st.session_state.current_sub}")
    else: st.markdown(st.session_state.lesson_txt)
    
    # התפריט התחתון שהוחזר
    st.markdown("---")
    if st.button("⬅️ חזרה לבחירת נושא"): 
        st.session_state.step = "study"
        st.session_state.lesson_txt = ""
        st.rerun()

elif st.session_state.step == "exam_run":
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 180 - int(elapsed))
    if rem <= 0: st.session_state.step = "results"; st.rerun()
    mins, secs = divmod(rem, 60)
    st.markdown(f'<div class="timer-box">⏳ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    idx = st.session_state.current_q_idx
    q = st.session_state.exam_qs[idx]
