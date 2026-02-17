# Project: מתווך בקליק | Version: B04
# File: main.py
import streamlit as st
from syllabus_data import SYLLABUS
from styles import apply_styles, show_footer
from ai_engine import stream_lesson, fetch_quick_question

# הגדרות דף - חייב להיות ראשון
st.set_page_config(page_title="מתווך בקליק", layout="wide", page_icon="🏠")
apply_styles("B04")

# כותרת קבועה בראש הדף
st.title("🏠 מתווך בקליק")

# אתחול Session State
if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "selected_topic": None,
        "current_sub": None, "lesson_txt": "", "q_data": None
    })

# הצגת שם משתמש בפינה (כפי שהיה קודם)
if st.session_state.user:
    st.markdown(f"<div style='text-align: left; color: gray;'>משתמש: {st.session_state.user}</div>", unsafe_allow_html=True)

# לוגיקת דפים
if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.user = u
        st.session_state.step = "menu"
        st.rerun()

elif st.session_state.step == "menu":
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("📚 לימוד לפי נושאים"):
            st.session_state.step = "study_select"
            st.rerun()
    with c2:
        if st.button("⏱️ מבחן מלא"):
            st.session_state.step = "exam_mode"
            st.rerun()

elif st.session_state.step == "study_select":
    st.subheader("בחר נושא:")
    sel = st.selectbox("", ["בחר..."] + list(SYLLABUS.keys()))
    c1, c2, _ = st.columns([0.8, 0.8, 6])
    with c1:
        if sel != "בחר..." and st.button("טען נושא"):
            st.session_state.selected_topic = sel
            st.session_state.step = "lesson_view"
            st.rerun()
    with c2:
        if st.button("🔙 חזרה"):
            st.session_state.step = "menu"
            st.rerun()

elif st.session_state.step == "lesson_view":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    
    # כפתורי תת-נושאים צמודים לימין
    subs = SYLLABUS.get(topic, [])
    sub_cols = st.columns(min(len(subs), 6))
    for i, s in enumerate(subs):
        if sub_cols[i % 6].button(s, key=f"sub_{i}"):
            st.session_state.update({"current_sub": s, "lesson_txt": "LOADING", "q_data": None})
            st.rerun()

    if st.session_state.lesson_txt == "LOADING":
        st.divider()
        response = stream_lesson(topic, st.session_state.current_sub)
        if response:
            full_txt = ""
            placeholder = st.empty()
            for chunk in response:
                if chunk.text:
                    full_txt += chunk.text
                    placeholder.markdown(f"<div style='direction: rtl; text-align: right;'>{full_txt}▌</div>", unsafe_allow_html=True)
            placeholder.markdown(f"<div style='direction: rtl; text-align: right;'>{full_txt}</div>", unsafe_allow_html=True)
            st.session_state.lesson_txt = full_txt

    elif st.session_state.lesson_txt:
        st.divider()
        st.markdown(f"<div style='direction: rtl; text-align: right;'>{st.session_state.lesson_txt}</div>", unsafe_allow_html=True)
        
        # תפריט תחתון בתוך דף השיעור
        st.write("---")
        b1, b2, _ = st.columns([1.5, 1.5, 5])
        with b1:
            if st.button("📝 שאלת בדיקת הבנה"):
                st.session_state.q_data = fetch_quick_question(topic, st.session_state.current_sub)
                st.rerun()
        with b2:
            if st.button("🏠 לתפריט הראשי"):
                st.session_state.step = "menu"
                st.rerun()

        if st.session_state.q_data:
            st.info(f"**שאלה:** {st.session_state.q_data['q']}")
            ans = st.radio("בחר תשובה:", st.session_state.q_data['options'])
            if st.button("בדיקת תשובה"):
                if ans == st.session_state.q_data['correct']:
                    st.success(f"נכון! {st.session_state.q_data['explain']}")
                else:
                    st.error(f"לא מדויק. {st.session_state.q_data['explain']}")

# הצגת הפוטר רק בסוף הכל
show_footer("B04")
