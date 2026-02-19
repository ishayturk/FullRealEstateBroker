import streamlit as st
from logic import ExamLogic
import os

# הגדרות דף
st.set_page_config(page_title="מערכת בחינות - פרוטוקול C-01", dir="rtl")

# וידוא שהקובץ קיים לפני טעינה
file_path = "exams_data/test_may1_v1_2025.json"

if not os.path.exists(file_path):
    st.error(f"קובץ המבחן לא נמצא בנתיב: {file_path}")
else:
    # אתחול הלוגיקה בזיכרון של הסשן
    if 'exam' not in st.session_state:
        st.session_state.exam = ExamLogic(file_path)

    exam = st.session_state.exam
    current_q = exam.get_current_question()

    if current_q:
        st.title(f"שאלה {exam.current_index + 1} מתוך {len(exam.questions)}")
        
        # תצוגת השאלה (שימוש במפתח question_text מהפרוטוקול)
        st.subheader(current_q.get('question_text', 'שאלה ללא תוכן'))
        
        # הצגת האפשרויות
        options = current_q.get('options', [])
        choice = st.radio("בחר את התשובה הנכונה:", options, key=f"q_{exam.current_index}")

        # כפתור מעבר
        if st.button("המשך לשאלה הבאה"):
            exam.next_question()
            st.rerun()
    else:
        st.success("הבחינה הסתיימה!")
        if st.button("התחל מחדש"):
            st.session_state.exam.current_index = 0
            st.rerun()
