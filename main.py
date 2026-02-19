import streamlit as st
from logic import ExamLogic
import os

# הגדרת כיוון כתיבה לימין (עבור עברית)
st.set_page_config(page_title="מערכת בחינות", dir="rtl")

# נתיב לקובץ לפי הפרוטוקול
FILE_PATH = "exams_data/test_may1_v1_2025.json"

# בדיקה שהקובץ קיים בתיקייה הנכונה
if not os.path.exists(FILE_PATH):
    st.error(f"שגיאה: הקובץ לא נמצא בנתיב {FILE_PATH}")
else:
    # ניהול מצב השאלות ב-Session State
    if 'exam' not in st.session_state:
        st.session_state.exam = ExamLogic(FILE_PATH)

    exam = st.session_state.exam
    current_q = exam.get_current_question()

    if current_q:
        st.title(f"שאלה {exam.current_index + 1} מתוך {len(exam.questions)}")
        
        # הצגת השאלה
        st.markdown(f"### {current_q.get('question_text', 'טקסט חסר')}")
        
        # בחירת תשובה
        options = current_q.get('options', [])
        st.radio("בחר תשובה:", options, key=f"q_radio_{exam.current_index}")

        # כפתור מעבר
        if st.button("המשך לשאלה הבאה"):
            exam.next_question()
            st.rerun()
    else:
        st.success("סיימת את המבחן!")
        if st.button("התחל מחדש"):
            st.session_state.exam.current_index = 0
            st.rerun()
