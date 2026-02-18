# Version: C-07 | ID: C-01 | Anchor: 1218-G2
import streamlit as st
import pandas as pd
import time
import os
from exam_logic import prepare_question_data
from ui_utils import render_rtl, show_results

render_rtl()

# אתחול משתני מצב
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'loaded_count' not in st.session_state: st.session_state.loaded_count = 5

@st.cache_data
def load_data():
    if not os.path.exists("exam_data.csv"):
        # יצירת שלד קובץ אם חסר
        df = pd.DataFrame({
            'שאלה': [f'שאלה {i}' for i in range(1, 26)],
            'תשובה_נכונה': ["1"] * 25
        })
        df.to_csv("exam_data.csv", index=False, encoding='utf-8-sig')
    return pd.read_csv("exam_data.csv")

df = load_data()

# --- ניווט דפים ---

if st.session_state.page == 'home':
    c1, c2 = st.columns(2)
    if c1.button("📚 לימודים", use_container_width=True):
        st.session_state.page = 'study'; st.rerun()
    if c2.button("📝 בחינה", use_container_width=True):
        st.session_state.page = 'exam'; st.session_state.start_time = time.time(); st.rerun()

elif st.session_state.page == 'study':
    if st.button("🔙 חזור"): st.session_state.page = 'home'; st.rerun()
    st.write("כאן יופיע תוכן הלימודים.")

elif st.session_state.page == 'exam':
    # לוגיקת בחינה חסכונית (Lazy Loading)
    if 'exam_data' not in st.session_state:
        st.session_state.exam_data = prepare_question_data(df, 0, 25)

    # טיימר
    rem = max(0, 180 - (time.time() - st.session_state.start_time))
    st.sidebar.metric("⏳ זמן", f"{int(rem//60):02d}:{int(rem%60):02d}")
    if rem <= 0: st.session_state.page = 'results'; st.rerun()

    # בחירת שאלה מתוך מה שנטען
    q_num = st.sidebar.radio("שאלה:", range(1, st.session_state.loaded_count + 1))
    q_idx = q_num - 1
    
    st.write(st.session_state.exam_data[q_idx]['שאלה'])
    ans = st.radio("בחר:", ["1","2","3","4"], 
                   index=["1","2","3","4"].index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
                   key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = ans

    # שליטה בטעינה
    if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
        if st.button("טען עוד 5 שאלות"):
            st.session_state.loaded_count += 5; st.rerun()
    elif st.session_state.loaded_count == 25:
        if st.button("סיום והגשה"):
            st.session_state.page = 'results'; st.rerun()

elif st.session_state.page == 'results':
    show_results(st.session_state.answers, st.session_state.exam_data)
    if st.button("🔙 חזרה לתפריט"):
        for k in ['exam_data', 'answers', 'loaded_count']: st.session_state.pop(k, None)
        st.session_state.page = 'home'; st.rerun()
