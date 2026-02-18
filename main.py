# Version: C-02
# Based on Anchor: 1218-G2
# Description: Main entry point with 3-minute test timer and Lazy Loading logic.

import streamlit as st
import pandas as pd
import time
from exam_logic import get_unique_exam, prepare_question_data
from UI_UTILS import show_instructions, render_navigation, show_results_summary

st.set_page_config(page_title="מערכת בחינות C-02", layout="wide")

# הגדרת זמן בדיקה (180 שניות)
TEST_TIME_SEC = 3 * 60 

# אתחול Session State
if 'step' not in st.session_state:
    st.session_state.step = 'instructions'
if 'finished_exams' not in st.session_state:
    st.session_state.finished_exams = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'loaded_count' not in st.session_state:
    st.session_state.loaded_count = 5

@st.cache_data
def load_data():
    try:
        # הקפד שיהיה קובץ כזה בתיקייה
        return pd.read_csv("exam_data.csv")
    except Exception as e:
        st.error(f"שגיאה בטעינת הקובץ: {e}")
        return pd.DataFrame()

df = load_data()

# --- שלב ההוראות ---
if st.session_state.step == 'instructions':
    if 'current_exam_col' not in st.session_state:
        st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
    
    if st.session_state.current_exam_col:
        show_instructions()
    else:
        st.warning("ביצעת כבר את כל המבחנים הזמינים בסשן זה.")

# --- שלב המבחן ---
elif st.session_state.step == 'exam':
    # חישוב זמן נותר
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, TEST_TIME_SEC - elapsed)
    
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("⏳ זמן נותר", f"{mins:02d}:{secs:02d}")
    
    if remaining <= 0:
        st.error("⌛ הזמן נגמר! המבחן ננעל.")
        if st.button("עבור לתוצאות"):
            st.session_state.step = 'results'
            st.rerun()
        st.stop()

    # הכנת השאלות הנוכחיות (טעינה מדורגת)
    current_questions = prepare_question_data(df, st.session_state.current_exam_col, 0, st.session_state.loaded_count)
    
    is_mobile = st.sidebar.toggle("מצב נייד", value=False)
    q_num = render_navigation(len(current_questions), is_mobile)
    q_idx = q_num - 1
    
    st.subheader(f"שאלה {q_num}")
    st.write(current_questions[q_idx]['שאלה'])
    
    # ניהול תשובות - מניח שהאפשרויות הן 1, 2, 3, 4
    options = ["1", "2", "3", "4"]
    current_ans = st.session_state.answers.get(q_idx, None)
    idx = options.index(current_ans) if current_ans in options else None
    
    choice = st.radio("בחר תשובה:", options, index=idx, key=f"q_radio_{q_idx}")
    st.session_state.answers[q_idx] = choice

    st.divider()
    
    # שליטה בהתקדמות
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
            if st.button("טען 5 שאלות נוספות"):
                st.session_state.loaded_count += 5
                st.rerun()
    with col2:
        if st.session_state.loaded_count == 25:
            if st.button("סיים בחינה והגש"):
                st.session_state.finished_exams.append(st.session_state.current_exam_col)
                st.session_state.step = 'results'
                st.rerun()

# --- שלב התוצאות ---
elif st.session_state.step == 'results':
    full_exam = prepare_question_data(df, st.session_state.current_exam_col, 0, 25)
    show_results_summary(st.session_state.answers, full_exam)
    
    if st.button("חזרה למבחן חדש"):
        # ניקוי סשן לקראת המבחן הבא
        for key in ['current_exam_col', 'answers', 'loaded_count', 'start_time']:
            st.session_state.pop(key, None)
        st.session_state.step = 'instructions'
        st.rerun()
