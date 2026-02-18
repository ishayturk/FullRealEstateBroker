# Version: C-06.1 | ID: C-01
import streamlit as st
import pandas as pd
import time
import os
import random
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

st.set_page_config(layout="wide")

# RTL Fix
st.markdown("""<style>
    .stApp, div[role="radiogroup"], section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
</style>""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'finished_exams' not in st.session_state: st.session_state.finished_exams = []

@st.cache_data
def load_data():
    if not os.path.exists("exam_data.csv"):
        data = {
            'שאלה': [f'שאלה {i}' for i in range(1, 26)],
            'מועד_א': [str(random.randint(1,4)) for _ in range(25)],
            'תשובה_נכונה': ["1"] * 25
        }
        pd.DataFrame(data).to_csv("exam_data.csv", index=False, encoding='utf-8-sig')
    return pd.read_csv("exam_data.csv")

df = load_data()

if st.session_state.page == 'home':
    c1, c2 = st.columns(2)
    if c1.button("📚 לימודים", use_container_width=True):
        st.session_state.page = 'study'; st.rerun()
    if c2.button("📝 בחינה", use_container_width=True):
        st.session_state.page = 'exam'; st.session_state.step = 'instructions'; st.rerun()

elif st.session_state.page == 'study':
    if st.button("🔙"): st.session_state.page = 'home'; st.rerun()
    st.write("תוכן לימודי")

elif st.session_state.page == 'exam':
    if st.session_state.step == 'instructions':
        if 'current_exam_col' not in st.session_state:
            st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
        if st.session_state.current_exam_col:
            show_instructions()
            if st.button("ביטול"): st.session_state.page = 'home'; st.rerun()
        else:
            st.warning("אין מבחנים"); st.button("חזרה", on_click=lambda: st.session_state.update(page='home'))

    elif st.session_state.step == 'exam':
        if 'current_exam_data' not in st.session_state:
            st.session_state.current_exam_data = prepare_question_data(df, st.session_state.current_exam_col, 0, 25)
            st.session_state.answers = {}; st.session_state.loaded_count = 5

        rem = max(0, 180 - (time.time() - st.session_state.start_time))
        st.sidebar.metric("זמן", f"{int(rem//60):02d}:{int(rem%60):02d}")
        if rem <= 0: st.session_state.step = 'results'; st.rerun()

        q_num = render_navigation(st.session_state.loaded_count, st.sidebar.toggle("נייד"))
        q_idx = q_num - 1
        st.write(st.session_state.current_exam_data[q_idx]['שאלה'])
        
        ans = st.radio("תשובה:", ["1","2","3","4"], 
                       index=["1","2","3","4"].index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
                       key=f"q_{q_idx}")
        st.session_state.answers[q_idx] = ans

        if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
            if st.button("טען עוד 5"): st.session_state.loaded_count += 5; st.rerun()
        elif st.session_state.loaded_count == 25:
            if st.button("הגש"):
                st.session_state.finished_exams.append(st.session_state.current_exam_col)
                st.session_state.step = 'results'; st.rerun()

    elif st.session_state.step == 'results':
        show_results_summary(st.session_state.answers, st.session_state.current_exam_data)
        if st.button("סיום"):
            for k in ['current_exam_col', 'answers', 'loaded_count', 'start_time', 'current_exam_data']:
                st.session_state.pop(k, None)
            st.session_state.page = 'home'; st.rerun()
