import streamlit as st
from logic import ExamManager
import time

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

st.set_page_config(page_title="מערכת בחינות", layout="wide")

# פתרון ליישור לימין (RTL) - זה יסדר את הכותרת והטקסט
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    /* יישור כותרות ספציפי */
    h1, h2, h3, p, span { text-align: right !format; direction: rtl !format; }
    /* יישור כפתורי רדיו */
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

exam = ExamManager()

if 'exam_started' not in st.session_state:
    if exam.load_exam_from_json():
        info = st.session_state.full_exam_data['exam_info']
        # כותרת המבחן
        st.title(info['title'])
        st.write(info['instructions'])
        
        if not st.session_state.questions:
            exam.fetch_batch(0)
            
        if st.button("התחל בחינה"):
            st.session_state.exam_started = True
            st.rerun()
else:
    q_idx = st.session_state.get('current_q_idx', 0)
    questions = st.session_state.questions
    
    if q_idx < len(questions):
        q_data = questions[q_idx]
        st.subheader(f"שאלה {q_idx + 1}")
        st.info(q_data['q'])
        
        st.radio("בחר תשובה:", q_data['o'], key=f"q_{q_idx}")
        
        if st.button("הבא"):
            st.session_state.current_q_idx = q_idx + 1
            if st.session_state.current_q_idx == len(questions):
                exam.fetch_batch(len(questions))
            st.rerun()
