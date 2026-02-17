# Project: מתווך בקליק | Version: B04
# File: main.py
import streamlit as st
from syllabus_data import SYLLABUS
from styles import apply_styles, show_footer
from ai_engine import stream_lesson, fetch_quick_question

# הגדרות דף בסיסיות
st.set_page_config(page_title="מתווך בקליק", layout="wide", page_icon="🏠")
apply_styles("B04")

# --- כותרת קבועה (לא נעלמת) ---
st.title("🏠 מתווך בקליק")

# אתחול Session State
if "step" not in st.session_state:
    st.session_state.update({
        "user": None,
        "step": "login",
        "selected_topic": None,
        "current_sub": None,
        "lesson_txt": "",
        "q_data": None,
        "show_ans": False
    })

# --- דף כניסה ---
if st.session_state.step == "login":
    col_login, _ = st.columns([2, 3])
    with col_login:
        u = st.text_input("שם מלא:")
        if st.button("כניסה") and u:
            st.session_state.user = u
            st.session_state.step = "menu"
            st.rerun()

# --- תפריט ראשי ---
elif st.session_state.step == "menu":
    st.subheader(f"שלום, {st.session_state.user}")
    # כפתורים בגודל טבעי, אחד ליד השני
    c1, c2, _ = st.columns([1.2, 1.2, 5])
    with c1:
        if st.button("📚 לימוד לפי נושאים"):
            st.session_state.step = "study_select"
            st.rerun()
    with c2:
        if st.button("⏱️ מבחן מלא"):
            st.session_state.step = "exam_mode"
            st.rerun()

# --- בחירת נושא ---
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

# --- דף שיעור ותת-נושאים ---
elif st.session_state.step == "lesson_view":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    
    # הצגת תת-נושאים בשורה
    subs = SYLLABUS.get(topic, [])
    sub_cols = st.columns(min(len(subs), 6))
    for i, s in enumerate(subs):
        if sub_cols[i % 6].button(s, key=f"sub_{i}"):
            st.session_state.update({
                "current_sub": s,
                "lesson_txt": "LOADING",
                "q_data": None,
                "show_ans": False
            })
            st.rerun()

    if st.session_state.lesson_txt == "LOADING":
        st.divider()
        st.subheader(st.session_state.current_sub)
        response = stream_lesson(topic, st.session_state.current_sub)
        if response:
            full_txt = ""
            placeholder = st.empty()
            for chunk in response:
                if chunk.text:
                    full_txt += chunk.text
                    placeholder.markdown(full_txt + "▌")
            placeholder.markdown(full_txt)
            st.session_state.lesson_txt = full_txt
        else:
            st.error("לא התקבל מענה מה-AI. בדוק את המפתח ב-Secrets.")

    elif st.session_state.lesson_txt:
        st.divider()
        st.subheader(st.session_state.current_sub)
        st.markdown(st.session_state.lesson_txt)
        
        # כפתורי פעולה בתחתית כל תת-שיעור
        st.write("---")
        b1, b2, _ = st.columns([1.5, 1.5, 5])
        with b1:
            if st.button("📝 שאלת בדיקת הבנה"):
                with st.spinner("מכין שאלה..."):
                    st.session_state.q_data = fetch_quick_question(topic, st.session_state.current_sub)
                    st.rerun()
        with b2:
            if st.button("🏠 לתפריט הראשי"):
                st.session_state.step = "menu"
                st.rerun()
        
        # תצוגת השאלון
        if st.session_state.q_data:
            st.info(f"**שאלה:** {st.session_state.q_data['q']}")
            ans = st.radio("בחר תשובה:", st.session_state.q_data['options'], key="quiz_radio")
            if st.button("בדיקת תשובה"):
                if ans == st.session_state.q_data['correct']:
                    st.success(f"נכון! {st.session_state.q_data['explain']}")
                else:
                    st.error(f"לא מדויק. {st.session_state.q_data['explain']}")

# --- דף מבחן מלא ---
elif st.session_state.step == "exam_mode":
    st.header("⏱️ סימולציית מבחן מלא")
    st.info("כאן יופיעו שאלות המבחן המלא בקרוב.")
    if st.button("🏠 לתפריט הראשי"):
        st.session_state.step = "menu"
        st.rerun()

show_footer("B04")
