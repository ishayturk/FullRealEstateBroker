# Project: מתווך בקליק | Version: B03
# File: main.py
import streamlit as st
from syllabus_data import SYLLABUS
from styles import apply_styles, show_footer
from ai_engine import stream_lesson, fetch_quick_question

# הגדרות דף
st.set_page_config(page_title="מתווך בקליק", layout="wide")
apply_styles("B03")

# --- כותרת קבועה שנשארת תמיד למעלה ---
st.title("🏠 מתווך בקליק")
st.write("") # רווח קטן

# אתחול Session State
if "step" not in st.session_state:
    st.session_state.update({
        "user": None,
        "step": "login",
        "selected_topic": None,
        "current_sub": None,
        "lesson_txt": "",
        "quiz_active": False,
        "q_data": None,
        "q_count": 0,
        "show_ans": False
    })

# --- דף כניסה ---
if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.user = u
        st.session_state.step = "menu"
        st.rerun()

# --- תפריט ראשי ---
elif st.session_state.step == "menu":
    st.subheader(f"שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים", use_container_width=True):
            st.session_state.step = "study_select"
            st.rerun()
    with c2:
        if st.button("⏱️ מבחן מלא", use_container_width=True):
            st.session_state.step = "exam_mode"
            st.rerun()

# --- בחירת נושא לימוד ---
elif st.session_state.step == "study_select":
    st.subheader("בחר נושא:")
    sel = st.selectbox("", ["בחר..."] + list(SYLLABUS.keys()))
    if sel != "בחר..." and st.button("טען נושא"):
        st.session_state.selected_topic = sel
        st.session_state.step = "lesson_view"
        st.rerun()
    if st.button("🔙 חזרה"):
        st.session_state.step = "menu"
        st.rerun()

# --- דף שיעור ---
elif st.session_state.step == "lesson_view":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    
    subs = SYLLABUS.get(topic, [])
    cols = st.columns(len(subs) if len(subs) > 0 else 1)
    for i, s in enumerate(subs):
        if cols[i % len(cols)].button(s, key=f"sub_{i}"):
            st.session_state.update({
                "current_sub": s,
                "lesson_txt": "LOADING",
                "quiz_active": False,
                "q_data": None
            })
            st.rerun()

    if st.session_state.lesson_txt == "LOADING":
        st.divider()
        st.subheader(st.session_state.current_sub)
        response = stream_lesson(topic, st.session_state.current_sub)
        
        if response:
            full_txt = ""
            placeholder = st.empty()
            try:
                for chunk in response:
                    if chunk.text:
                        full_txt += chunk.text
                        placeholder.markdown(full_txt + "▌")
                placeholder.markdown(full_txt)
                st.session_state.lesson_txt = full_txt
            except Exception as e:
                st.error(f"הזרמת התוכן נפסקה. נסה שוב.")
        else:
            st.error("לא התקבל מענה מה-AI. בדוק את המפתח ב-Secrets.")

    elif st.session_state.lesson_txt:
        st.divider()
        st.subheader(st.session_state.current_sub)
        st.markdown(st.session_state.lesson_txt)

    # כפתורי ניווט למטה
    st.write("")
    f1, f2 = st.columns([1, 5])
    with f1:
        if st.button("🏠 תפריט"):
            st.session_state.step = "menu"
            st.rerun()

show_footer("B03")
