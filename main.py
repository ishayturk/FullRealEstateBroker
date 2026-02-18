# main.py | Version: C-02
import streamlit as st
from app_data import TOPICS_DATA
from ai_logic import stream_ai_lesson
from ui_utils import apply_design, navigation_footer
from exam_logic import run_exam

st.set_page_config(page_title="מתווך בקליק", layout="centered")

if "step" not in st.session_state:
    st.session_state.update({
        "user": None,
        "step": "login",
        "lesson_txt": "",
        "current_sub": None
    })

apply_design()

if st.session_state.step == "login":
    st.title("🏠 מתווך בקליק")
    user_input = st.text_input("שם מלא:")
    if st.button("כניסה") and user_input:
        st.session_state.user = user_input
        st.session_state.step = "menu"
        st.rerun()

elif st.session_state.step == "menu":
    st.header(f"שלום, {st.session_state.user}")
    
    if st.button("📚 לימוד לפי נושאים"):
        st.session_state.step = "study"
        st.rerun()
        
    if st.button("📝 מבחן תרגול מקיף"):
        st.session_state.step = "exam"
        st.rerun()

elif st.session_state.step == "study":
    st.subheader("בחר נושא לימוד")
    selected_main = st.selectbox("בחר נושא:", ["בחר נושא"] + list(TOPICS_DATA.keys()))
    
    if selected_main != "בחר נושא":
        for sub in TOPICS_DATA[selected_main]:
            if st.button(sub, key=f"btn_{sub}"):
                st.session_state.current_sub = sub
                st.session_state.step = "lesson_run"
                st.session_state.lesson_txt = "LOADING"
                st.rerun()
    navigation_footer()

elif st.session_state.step == "lesson_run":
    st.subheader(f"📖 שיעור: {st.session_state.current_sub}")
    if st.session_state.lesson_txt == "LOADING":
        full_text = ""
        placeholder = st.empty()
        response = stream_ai_lesson(st.session_state.current_sub)
        if response:
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            st.session_state.lesson_txt = full_text
    else:
        st.markdown(st.session_state.lesson_txt)
    navigation_footer()

elif st.session_state.step == "exam":
    run_exam()
    navigation_footer()
