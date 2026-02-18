# Version: C-05.1
# ID: C-01
# Description: Main entry with Auto-Data-Generation. 
# Fixed SyntaxError in string literal for "נדל"ן".

import streamlit as st
import pandas as pd
import time
import os
import random
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

st.set_page_config(page_title="מערכת בחינות C-05.1", layout="wide")

# הגדרת זמן מבחן - 3 דקות (180 שניות)
TEST_TIME_SEC = 3 * 60 

# בדיקה/יצירת קובץ נתונים כדי למנוע שגיאת "File Not Found"
if not os.path.exists("exam_data.csv"):
    data = {
        'שאלה': [f'שאלת נדל"ן מספר {i}' for i in range(1, 26)],
        'מועד_א': [str(random.randint(1, 4)) for _ in range(25)],
        'מועד_ב': [str(random.randint(1, 4)) for _ in range(25)],
        'תשובה_נכונה': ["1"] * 25
    }
    pd.DataFrame(data).to_csv("exam_data.csv", index=False, encoding='utf-8-sig')

# אתחול Session State (לכל משתמש בנפרד)
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
    return pd.read_csv("exam_data.csv")

df = load_data()

# --- ניהול שלבי האפליקציה ---

if st.session_state.step == 'instructions':
    if 'current_exam_col' not in st.session_state:
        st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
    
    if st.session_state.current_exam_col:
        show_instructions()
    else:
        st.success("🎉 כל המבחנים הזמינים הושלמו!")
        if st.button("אתחל סשן מחדש"):
            st.session_state.finished_exams = []
            st.rerun()

elif st.session_state.step == 'exam':
    # הכנת הנתונים למבחן הנוכחי (On the fly)
    if st.session_state.current_exam_data is None:
        st.session_state.current_exam_data = prepare_question_data(
            df, st.session_state.current_exam_col, 0, 25
        )

    # ניהול טיימר
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, TEST_TIME_SEC - elapsed)
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("⏳ זמן נותר", f"{mins:02d}:{secs:02d}")
    
    if remaining <= 0:
        st.error("⌛ הזמן הסתיים!")
