# Version: C-05 | ID: C-01
import streamlit as st
import pandas as pd
import time
import os
import random
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

st.set_page_config(page_title="מערכת בחינות C-05", layout="wide")
TEST_TIME_SEC = 3 * 60 

# יצירת קובץ אם חסר (פעם אחת עבור כל המשתמשים)
if not os.path.exists("exam_data.csv"):
    data = {
        'שאלה': [f"שאלת נדל"ן מספר {i}" for i in range(1, 26)],
        'מועד_א': [str(random.randint(1,4)) for _ in range(25)],
        'מועד_ב': [str(random.randint(1,4)) for _ in range(25)],
        'תשובה_נכונה': ["1"] * 25
    }
    pd.DataFrame(data).to_csv("exam_data.csv", index=False, encoding='utf-8-sig')

# אתחול סשן (פרטי לכל משתמש)
for key, val in [('step','instructions'), ('finished_exams',[]), ('answers',{}), ('loaded_count',5)]:
    if key not in st.session_state: st.session_state[key] = val

@st.cache_data
def load_data(): return pd.read_csv("exam_data.csv")
df = load_data()

if st.session_state.step == 'instructions':
    if 'current_exam_col' not in st.session_state:
        st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
    show_instructions()

elif st.session_state.step == 'exam':
    if 'current_exam_data' not in st.session_state or st.session_state.current_exam_data is None:
        st.session_state.current_exam_data = prepare_question_data(df, st.session_state.current_exam_col, 0, 25)

    rem = max(0, TEST_TIME_SEC - (time.time() - st.session_state.start_time))
    st.sidebar.metric("⏳ זמן נותר", f"{int(rem//60):02d}:{int(rem%60):02d}")
    
    if rem <= 0:
        st.session_state.step = 'results'; st.rerun()

    q_num = render_navigation(st.session_state.loaded_count, st.sidebar.toggle("נייד"))
    q_idx = q_num - 1
    st.subheader(f"שאלה {q_num} (מבחן: {st.session_state.current_exam_col})")
    st.write(st.session_state.current_exam_data[q_idx]['שאלה'])
    
    ans = st.radio("תשובה:", ["1","2","3","4"], 
                   index=["1","2","3","4"].index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
                   key=f"r_{q_idx}")
    st.session_state.answers[q_idx] = ans

    if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
        if st.button("טען עוד 5"): st.session_state.loaded_count += 5; st.rerun()
    elif st.session_state.loaded_count == 25:
        if st.button("הגש בחינה"):
            st.session_state.finished_exams.append(st.session_state.current_exam_col)
            st.session_state.step = 'results'; st.rerun()

elif st.session_state.step == 'results':
    show_results_summary(st.session_state.answers, st.session_state.current_exam_data)
    if st.button("מבחן חדש"):
        for k in ['current_exam_col','answers','loaded_count','current_exam_data']: st.session_state.pop(k, None)
        st.session_state.step = 'instructions'; st.rerun()
