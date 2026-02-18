import streamlit as st
import pandas as pd
import time
import os
import random
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

# הגדרת עמוד ויישור לימין
st.set_page_config(page_title="מערכת בחינות מתווכים", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

TEST_TIME_SEC = 3 * 60 

# יצירת קובץ נתונים אם חסר
if not os.path.exists("exam_data.csv"):
    data = {
        'שאלה': [f'שאלת נדל"ן מספר {i}' for i in range(1, 26)],
        'מועד_א': [str(random.randint(1, 4)) for _ in range(25)],
        'מועד_ב': [str(random.randint(1, 4)) for _ in range(25)],
        'תשובה_נכונה': ["1"] * 25
    }
    pd.DataFrame(data).to_csv("exam_data.csv", index=False, encoding='utf-8-sig')

# אתחול Session State
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

# --- זרימת הבחינה ---

if st.session_state.step == 'instructions':
    if 'current_exam_col' not in st.session_state:
        st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
    
    if st.session_state.current_exam_col:
        show_instructions()
    else:
        st.warning("כל המבחנים הזמינים הושלמו.")

elif st.session_state.step == 'exam':
    if st.session_state.current_exam_data is None:
        st.session_state.current_exam_data = prepare_question_data(
            df, st.session_state.current_exam_col, 0, 25
        )

    # טיימר
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, TEST_TIME_SEC - elapsed)
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("⏳ זמן נותר", f"{mins:02d}:{secs:02d}")
    
    if remaining <= 0:
        st.session_state.step = 'results'
        st.rerun()

    # ניווט וטעינה מדורגת
    is_mobile = st.sidebar.toggle("תצוגת נייד", value=False)
    q_num = render_navigation(st.session_state.loaded_count, is_mobile)
    q_idx = q_num - 1
    
    q_data = st.session_state.current_exam_data[q_idx]
    st.subheader(f"שאלה {q_num}")
    st.write(q_data['שאלה'])
    
    options = ["1", "2", "3", "4"]
    current_ans = st.session_state.answers.get(q_idx, None)
    radio_idx = options.index(current_ans) if current_ans in options else None
    
    choice = st.radio("בחר תשובה:", options, index=radio_idx, key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = choice

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
            if st.button("טען עוד 5 שאלות"):
                st.session_state.loaded_count += 5
                st.rerun()
    with col2:
        if st.session_state.loaded_count == 25:
            if st.button("הגש בחינה"):
                st.session_state.finished_exams.append(st.session_state.current_exam_col)
                st.session_state.step = 'results'
                st.rerun()

elif st.session_state.step == 'results':
    show_results_summary(st.session_state.answers, st.session_state.current_exam_data)
    if st.button("מבחן חדש"):
        for k in ['current_exam_col', 'answers', 'loaded_count', 'start_time', 'current_exam_data']:
            st.session_state.pop(k, None)
        st.session_state.step = 'instructions'
        st.rerun()
