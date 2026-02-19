# FILE-ID: C-01
import streamlit as st
from logic import ExamLogic
import time

# הגדרות עמוד
st.set_page_config(page_title="סימולטור מבחן מתווכים", layout="wide")

# אתחול לוגיקה
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()
    st.session_state.used_exams = []
    st.session_state.current_exam = None
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.start_time = None

def start_new_exam():
    filename, exam_data = st.session_state.logic.select_next_exam(st.session_state.used_exams)
    st.session_state.current_exam = exam_data
    st.session_state.used_exams.append(filename)
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.start_time = time.time()

# מסך פתיחה
if st.session_state.current_exam is None:
    st.title("ברוכים הבאים לסימולטור המבחן")
    st.header("מבחן סימולציה לרישיון מתווך")
    if st.button("התחל מבחן חדש"):
        start_new_exam()
        st.rerun()

# מסך מבחן פעיל
else:
    exam = st.session_state.current_exam
    q_idx = st.session_state.question_index
    questions = exam['questions']
    current_q = questions[q_idx]

    # כותרת קבועה לפי הפרוטוקול
    st.title(exam['display_title'])

    # תצוגת שעון ומיקום
    col1, col2 = st.columns([1, 4])
    with col1:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, st.session_state.logic.total_seconds - elapsed)
        st.metric("זמן נותר", st.session_state.logic.format_time(remaining))
    with col2:
        st.write(f"### שאלה {q_idx + 1} מתוך {len(questions)}")

    st.divider()

    # הצגת השאלה
    st.info(current_q['question_text'])

    # בחירת תשובה (שאלה אחת בכל פעם)
    current_ans = st.session_state.answers.get(str(q_idx), None)
    
    selected_opt = st.radio(
        "בחר את התשובה הנכונה:",
        current_q['options'],
        index=current_q['options'].index(current_ans) if current_ans in current_q['options'] else None,
        key=f"q_{q_idx}"
    )

    # שמירת התשובה בזיכרון
    if selected_opt:
        st.session_state.answers[str(q_idx)] = selected_opt

    st.divider()

    # כפתורי ניווט
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    
    with nav_col1:
        if q_idx > 0:
            if st.button("⬅️ שאלה קודמת"):
                st.session_state.question_index -= 1
                st.rerun()

    with nav_col3:
        if q_idx < len(questions) - 1:
            if st.button("שאלה הבאה ➡️"):
                st.session_state.question_index += 1
                st.rerun()
        else:
            if st.button("סיום מבחן וציון"):
                # כאן תבוא לוגיקת סיום (נבנה בהמשך אם תרצה)
                st.success("המבחן הסתיים! (לוגיקת הציון תופעל כאן)")
