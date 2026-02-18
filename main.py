import streamlit as st
from logic import ExamManager
import time

# ID: C-01 | Anchor: 1213 | Version: 1218-G7
# ממשק משתמש RTL תומך תיקיית exams_data

st.set_page_config(page_title="C-01 Exam System", layout="wide")
st.markdown("<style>.stApp { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

exam = ExamManager()

if 'exam_started' not in st.session_state:
    if exam.load_exam_from_json():
        info = st.session_state.full_exam_data['exam_info']
        st.title(f"📄 {info['title']} (C-01)")
        st.write(f"**הוראות:** {info['instructions']}")
        
        if not st.session_state.questions:
            exam.fetch_batch(0)
            
        if st.button("התחל בחינה"):
            st.session_state.exam_started = True
            st.session_state.start_time = time.time()
            st.session_state.current_q_idx = 0
            st.rerun()
else:
    q_idx = st.session_state.current_q_idx
    questions = st.session_state.questions
    
    # טיימר
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, (exam.time_limit * 60) - elapsed)
    st.sidebar.header(f"זמן נותר: {remaining // 60}:{remaining % 60:02d}")
    
    # טעינת המנה הבאה (5-5-5)
    if q_idx + 1 == len(questions) and len(questions) < exam.total_questions:
        exam.fetch_batch(len(questions))

    if q_idx < len(questions):
        q_data = questions[q_idx]
        st.subheader(f"שאלה {q_idx + 1} מתוך {exam.total_questions}")
        st.info(q_data['q'])
        
        choice = st.radio("בחר תשובה:", q_data['o'], key=f"q_{q_idx}")
        st.session_state.answers[q_idx] = choice

        col1, col2 = st.columns(2)
        with col1:
            if q_idx > 0 and st.button("הקודם"):
                st.session_state.current_q_idx -= 1
                st.rerun()
        with col2:
            if q_idx < exam.total_questions - 1:
                if st.button("הבא"):
                    st.session_state.current_q_idx += 1
                    st.rerun()
            else:
                if st.button("הגש מבחן"):
                    st.success("המבחן הסתיים בהצלחה!")
