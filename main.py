import streamlit as st
from logic import ExamManager
import time

st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stApp, h1, h2, h3, p, label, div, button { direction: rtl !important; text-align: right !important; }
    div[data-testid="stSidebarNav"] { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

exam = ExamManager(total_questions=10, time_limit=120)

if 'exam_started' not in st.session_state:
    st.title("מערכת בחינת המתווכים - C-01 (מתוקן)")
    if not st.session_state.questions:
        exam.fetch_batch(0) # מביא את 5 הראשונות בלובי
    
    confirm = st.checkbox("קראתי את ההנחיות ממשיך לכל הבחינה")
    if st.button("התחל בחינה", disabled=not confirm):
        st.session_state.exam_started = True
        st.session_state.start_time = time.time()
        st.session_state.current_idx = 0
        st.rerun()
else:
    # כאן הקוד של המבחן כפי שהוצג קודם עם הניווט בסידבר
    st.write(f"שאלה נוכחית: {st.session_state.current_idx + 1}")
    # ... (שאר הקוד מהגרסה הקודמת)
