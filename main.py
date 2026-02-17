# ==========================================
# Project: מתווך בקליק | Version: 1219-G2
# ==========================================
import streamlit as st
import google.generativeai as genai
import json, re, time, random

st.set_page_config(page_title="מתווך בקליק", layout="wide")
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

# CSS עם תמיכה בטיימר קבוע למעלה
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    .timer-box {
        position: fixed; top: 50px; left: 20px; background: #ff4b4b; color: white;
        padding: 10px; border-radius: 10px; z-index: 1000; font-weight: bold;
    }
    .v-footer { text-align: center; color: rgba(255, 255, 255, 0.1); font-size: 0.7em; }
</style>
""", unsafe_allow_html=True)

# פונקציות עזר (ללא שינוי מהותי מהעוגן)
def fetch_q_ai(topic):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        p = f"צור שאלה אמריקאית על {topic} למבחן המתווכים. החזר JSON תקני בלבד."
        res = m.generate_content(p).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        return json.loads(match.group().replace("'", '"')) if match else None
    except: return None

# מנגנון טעינת שאלות למבחן (5 בכל פעם)
def load_exam_chunk(count=5):
    new_qs = []
    topics = ["חוק המתווכים", "חוק המקרקעין", "חוק החוזים", "מיסוי", "תכנון ובנייה"]
    for _ in range(count):
        t = random.choice(topics)
        q = fetch_q_ai(t)
        if q: new_qs.append(q)
    return new_qs

# אתחול ה-State
if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "used_exams": [],
        "exam_qs": [], "current_q_idx": 0, "exam_active": False,
        "start_time": None, "exam_answers": {}
    })

st.title("🏠 מתווך בקליק")

# --- לוגיקת ניהול שלבים ---

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
        if st.button("⏱️ גש למבחן מלא (90 דק')"):
            # בדיקת כפילות: כאן נכניס בעתיד מזהה בחינה אמיתי
            st.session_state.update({
                "step": "exam_run", "exam_active": True, "exam_qs": [],
                "current_q_idx": 0, "start_time": time.time(), "exam_answers": {}
            })
            with st.spinner("מכין 5 שאלות ראשונות..."):
                st.session_state.exam_qs = load_exam_chunk(5)
            st.rerun()

elif st.session_state.step == "exam_run":
    # חישוב טיימר
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 5400 - int(elapsed)) # 90 דקות בשניות
    mins, secs = divmod(rem, 60)
    st.markdown(f'<div class="timer-box">⏳ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    if rem <= 0:
        st.error("נגמר הזמן!")
        st.session_state.step = "menu"; st.rerun()

    # הצגת שאלה נוכחית
    idx = st.session_state.current_q_idx
    qs = st.session_state.exam_qs

    if idx < len(qs):
        q = qs[idx]
        st.subheader(f"שאלה {idx + 1} מתוך 25")
        choice = st.radio(q['q'], q['options'], key=f"ex_{idx}", index=None)
        st.session_state.exam_answers[idx] = choice

        # כפתורי ניווט
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if idx > 0:
                if st.button("⬅️ הקודם"):
                    st.session_state.current_q_idx -= 1; st.rerun()
        with col2:
            if st.button("🏠 צא מהמבחן"):
                st.session_state.step = "menu"; st.rerun()
        with col3:
            label = "הבא ➡️" if idx < 24 else "🏁 הגש מבחן"
            if st.button(label):
                # טעינה ברקע: אם הגענו לסוף המנה וצריך עוד
                if idx == len(qs) - 1 and len(qs) < 25:
                    with st.spinner("טוען את 5 השאלות הבאות..."):
                        st.session_state.exam_qs += load_exam_chunk(5)
                
                if idx < 24:
                    st.session_state.current_q_idx += 1
                else:
                    st.success("המבחן הוגש בהצלחה!")
                    st.session_state.step = "menu"
                st.rerun()

st.markdown(f'<div class="v-footer">Version: 1219-G2</div>', unsafe_allow_html=True)
