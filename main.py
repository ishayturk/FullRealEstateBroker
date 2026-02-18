import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

# החזרת הסיידבר למצב פעיל
st.set_page_config(page_title="מערכת בחינות", layout="wide", initial_sidebar_state="expanded")

def apply_ui_fix():
    st.markdown("""
        <style>
            /* עיצוב הסיידבר שיהיה מיושר לימין */
            [data-testid="stSidebar"] {
                direction: rtl !important;
                background-color: #f8f9fa;
            }
            .main .block-container {
                max-width: 900px !important;
                margin: 0 auto !important;
                direction: rtl !important;
            }
            .stMarkdown, .stRadio label, p, div, h1, h2, h3, h4 {
                direction: rtl !important;
                text-align: right !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar(questions):
    with st.sidebar:
        st.title("ניווט בחינה")
        st.write("---")
        
        # יצירת גריד של כפתורים למעבר מהיר בין שאלות
        cols = st.columns(4)
        for i in range(len(questions)):
            col_idx = i % 4
            is_answered = str(questions[i]['id']) in st.session_state.answers
            label = f"{i+1}"
            if is_answered:
                label += " ✅"
            
            if cols[col_idx].button(label, key=f"nav_{i}"):
                st.session_state.q_idx = i
                st.rerun()
        
        st.write("---")
        if st.button("חזרה למצב לימוד 📖"):
            # לוגיקה למעבר ללימוד בלי להרוס את המבחן
            st.info("כאן תחובר לוגיקת הלימוד")

def main():
    apply_ui_fix()
    manager = ExamManager()
    exam_data = manager.load_exam()
    
    if not exam_data: return

    if 'current_step' not in st.session_state: st.session_state.current_step = 'intro'
    if 'answers' not in st.session_state: st.session_state.answers = {}

    if st.session_state.current_step == 'intro':
        render_intro(exam_data)
    elif st.session_state.current_step == 'exam':
        render_sidebar(exam_data['questions']) # הצגת הסיידבר רק בזמן מבחן
        render_timer()
        render_exam_flow(exam_data)
    elif st.session_state.current_step == 'feedback':
        render_feedback(exam_data)

# ... (שאר הפונקציות)
