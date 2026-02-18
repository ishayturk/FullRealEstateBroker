# Version: C-04
# ID: C-01
# Description: Main entry point. Manages session state, timer, and lazy loading.

import streamlit as st
import pandas as pd
import time
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

st.set_page_config(page_title="מערכת בחינות C-04", layout="wide")

# הגדרת זמן מבחן - 3 דקות
TEST_TIME_SEC = 3 * 60 

# אתחול Session State למניעת שגיאות הרצה
if 'step' not in st.session_state:
    st.session_state.step = 'instructions'
if 'finished_exams' not in st.session_state:
    st.session_state.finished_exams = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'loaded_count' not in st.session_state:
    st.session_state.loaded_count = 5
if 'current_exam_data' not in st.session_state:
    st.session_state.current_exam_data = None

@st.cache_data
def load_data():
    """טעינת בסיס הנתונים מה-CSV"""
    try:
        return pd.read_csv("exam_data.csv")
    except Exception as e:
        st.error(f"שגיאה קריטית: קובץ הנתונים לא נמצא ({e})")
        return pd.DataFrame()

df = load_data()

# --- ניהול שלבי האפליקציה ---

if st.session_state.step == 'instructions':
    if 'current_exam_col' not in st.session_state:
        st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
    if st.session_state.current_exam_col:
        show_instructions()
    else:
        st.warning("כל המבחנים הזמינים בסשן זה הושלמו.")

elif st.session_state.step == 'exam':
    # יצירת מפתח תשובות "און דה פליי" בתחילת המבחן
    if st.session_state.current_exam_data is None:
        st.session_state.current_exam_data = prepare_question_data(df, st.session_state.current_exam_col, 0, 25)

    # ניהול טיימר
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, TEST_TIME_SEC - elapsed)
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("⏳ זמן נותר", f"{mins:02d}:{secs:02d}")
    
    if remaining <= 0:
        st.error("⌛ הזמן הסתיים! המבחן ננעל.")
        if st.button("צפה בתוצאות"):
            st.session_state.step = 'results'
            st.rerun()
        st.stop()

    # טעינה מדורגת של שאלות
    is_mobile = st.sidebar.toggle("תצוגת נייד", value=False)
    q_num = render_navigation(st.session_state.loaded_count, is_mobile)
    q_idx = q_num - 1
    
    current_q = st.session_state.current_exam_data[q_idx]
    st.subheader(f"שאלה {q_num}")
    st.info(f"מבחן פעיל: {st.session_state.current_exam_col}")
    st.write(current_q['שאלה'])
    
    # ניהול תשובות
    options = ["1", "2", "3", "4"]
    current_ans = st.session_state.answers.get(q_idx, None)
    radio_idx = options.index(current_ans) if current_ans in options else None
    
    choice = st.radio("בחר תשובה:", options, index=radio_idx, key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = choice

    st.divider()
    
    # כפתורי ניווט וטעינה
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
            if st.button("טען 5 שאלות נוספות..."):
                st.session_state.loaded_count += 5
                st.rerun()
    with col2:
        if st.session_state.loaded_count == 25:
            if st.button("סיים והגש בחינה"):
                st.session_state.finished_exams.append(st.session_state.current_exam_col)
                st.session_state.step = 'results'
                st.rerun()

elif st.session_state.step == 'results':
    show_results_summary(st.session_state.answers, st.session_state.current_exam_data)
    if st.button("התחל מבחן חדש"):
        # ניקוי משתני סשן למבחן הבא
        for key in ['current_exam_col', 'answers', 'loaded_count', 'start_time', 'current_exam_data']:
            st.session_state.pop(key, None)
        st.session_state.step = 'instructions'
        st.rerun()
