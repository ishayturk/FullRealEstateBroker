# ID: C-01
# Based on Anchor: 1218-G2
# Main Entry Point: Managing session state, timer, and screen switching

import streamlit as st
import pandas as pd
from exam_logic import get_unique_exam, prepare_question_data
from UI_UTILS import show_instructions, render_navigation, show_results_summary

# הגדרות דף בסיסיות
st.set_page_config(page_title="מערכת בחינות C-01", layout="wide")

# אתחול Session State
if 'step' not in st.session_state:
    st.session_state.step = 'instructions'
if 'finished_exams' not in st.session_state:
    st.session_state.finished_exams = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'loaded_count' not in st.session_state:
    st.session_state.loaded_count = 5

# טעינת נתונים (סימולציה של CSV)
@st.cache_data
def load_data():
    # כאן תבוא הכתובת של ה-CSV שלך
    return pd.read_csv("exam_data.csv")

df = load_data()

# --- ניהול הצעדים (Steps) ---

if st.session_state.step == 'instructions':
    # הגרלת מבחן ברקע
    if 'current_exam_col' not in st.session_state:
        st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
    
    show_instructions()

elif st.session_state.step == 'exam':
    # הכנת השאלות שנטענו עד כה
    current_questions = prepare_question_data(
        df, 
        st.session_state.current_exam_col, 
        0, 
        st.session_state.loaded_count
    )
    
    # ניווט (תומך מובייל/דסקטופ)
    is_mobile = st.sidebar.checkbox("תצוגת נייד", value=False)
    q_idx = render_navigation(len(current_questions), is_mobile) - 1
    
    # הצגת השאלה הנוכחית
    st.subheader(f"שאלה {q_idx + 1}")
    st.write(current_questions[q_idx]['שאלה'])
    
    # בחירת תשובה (כאן יבואו האפשרויות מה-CSV)
    # לצורך הדוגמה:
    ans = st.radio("בחר תשובה:", ["א", "ב", "ג", "ד"], key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = ans
    
    # לוגיקת Lazy Loading - אם הגענו לשאלה האחרונה שנטענה
    if q_idx + 1 == st.session_state.loaded_count and st.session_state.loaded_count < 25:
        if st.button("טען שאלות נוספות"):
            st.session_state.loaded_count = min(25, st.session_state.loaded_count + 5)
            st.rerun()
            
    # כפתור סיום (מופיע רק בשאלה 25)
    if st.session_state.loaded_count == 25:
        if st.button("סיים בחינה והגש"):
            st.session_state.finished_exams.append(st.session_state.current_exam_col)
            st.session_state.step = 'results'
            st.rerun()

elif st.session_state.step == 'results':
    # משיכת כל 25 השאלות לבדיקה סופית
    full_exam = prepare_question_data(df, st.session_state.current_exam_col, 0, 25)
    show_results_summary(st.session_state.answers, full_exam)
    
    if st.button("חזרה למסך הראשי"):
        # איפוס נתונים לסבב הבא
        for key in ['current_exam_col', 'answers', 'loaded_count']:
            if key in st.session_state: del st.session_state[key]
        st.session_state.step = 'instructions'
        st.rerun()
