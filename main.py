# FILE-ID: C-01
import streamlit as st
from logic import ExamLogic
import time

# הגדרות עמוד ועיצוב RTL
st.set_page_config(page_title="סימולטור מבחן מתווכים", layout="wide")

# הזרקת CSS ליישור לימין והתאמות עיצוב
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: RTL; text-align: right; }
    div[role="radiogroup"] { direction: RTL; text-align: right; }
    p, h1, h2, h3, h4, li { text-align: right; direction: RTL; }
    [data-testid="stSidebar"] { direction: RTL; }
    /* כפתורים רחבים יותר לנייד */
    .stButton button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# אתחול מצב (Session State)
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()
    st.session_state.used_exams = []
    st.session_state.current_exam = None
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.start_time = None
    st.session_state.exam_finished = False

def start_new_exam():
    filename, exam_data = st.session_state.logic.select_next_exam(st.session_state.used_exams)
    st.session_state.current_exam = exam_data
    st.session_state.used_exams.append(filename)
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.start_time = time.time()
    st.session_state.exam_finished = False

# --- מסך פתיחה ---
if st.session_state.current_exam is None:
    st.title("מבחן סימולציה לרישיון מתווך")
    st.subheader("הוראות חשובות:")
    st.write("1. לא ניתן להתקדם לשאלה הבאה מבלי לסמן תשובה.")
    st.write("2. כפתור 'סיים בחינה' יופיע רק לאחר מענה על כל 25 השאלות.")
    if st.button("התחל בחינה"):
        start_new_exam()
        st.rerun()

# --- מסך מבחן פעיל ---
elif not st.session_state.exam_finished:
    exam = st.session_state.current_exam
    q_idx = st.session_state.question_index
    questions = exam['questions']
    current_q = questions[q_idx]
    
    # בדיקת זמן
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, st.session_state.logic.total_seconds - elapsed)
    if remaining <= 0:
        st.session_state.exam_finished = True
        st.rerun()

    # --- Sidebar (צף בנייד) ---
    with st.sidebar:
        st.header("מפת שאלות")
        # בדיקה אם כל השאלות נענו
        all_answered = len(st.session_state.answers) == len(questions)
        
        if all_answered:
            st.success("✅ ענית על כל השאלות!")
            if st.button("🏁 סיים בחינה כעת", key="finish_sidebar"):
                st.session_state.exam_finished = True
                st.rerun()
        
        st.divider()
        for i in range(len(questions)):
            answered = str(i) in st.session_state.answers
            label = f"שאלה {i+1} {'✅' if answered else '⚪'}"
            # ניתן לנווט רק למה שנענה או לנוכחית
            can_nav = answered or i == q_idx or (i > 0 and str(i-1) in st.session_state.answers)
            if st.button(label, key=f"nav_{i}", disabled=not can_nav):
                st.session_state.question_index = i
                st.rerun()

    # --- תצוגת השאלה ---
    st.title(exam['display_title'])
    st.write(f"**זמן נותר:** {st.session_state.logic.format_time(remaining)}")
    st.progress((q_idx + 1) / len(questions))
    
    st.subheader(f"שאלה {q_idx + 1}")
    st.info(current_q['question_text'])

    # רדיו לבחירת תשובה
    saved_ans = st.session_state.answers.get(str(q_idx))
    choice = st.radio(
        "בחר תשובה:", current_q['options'],
        index=current_q['options'].index(saved_ans) if saved_ans else None,
        key=f"radio_{q_idx}"
    )

    if choice:
        st.session_state.answers[str(q_idx)] = choice

    st.divider()

    # --- כפתורי ניווט תחתונים ---
    col_prev, col_finish, col_next = st.columns([1, 1, 1])
    
    has_answered_current = str(q_idx) in st.session_state.answers
    all_answered = len(st.session_state.answers) == len(questions)

    with col_prev:
        # מנוטרל בשאלה 1
        if st.button("⬅️ שאלה קודמת", disabled=(q_idx == 0)):
            st.session_state.question_index -= 1
            st.rerun()

    with col_next:
        # מנוטרל בשאלה 25 או אם לא ענה
        if q_idx < len(questions) - 1:
            if st.button("שאלה הבאה ➡️", disabled=not has_answered_current):
                st.session_state.question_index += 1
                st.rerun()
        else:
            st.button("שאלה הבאה ➡️", disabled=True)

    with col_finish:
        # מופיע רק כשכל השאלות נענו
        if all_answered:
            if st.button("🏁 סיים בחינה", type="primary"):
                st.session_state.exam_finished = True
                st.rerun()

# --- מסך תוצאות ---
else:
    st.success("המבחן הסתיים בהצלחה!")
    st.balloons()
    # לוגיקת חישוב ציון תתווסף כאן
    if st.button("חזרה לתפריט"):
        st.session_state.current_exam = None
        st.rerun()
