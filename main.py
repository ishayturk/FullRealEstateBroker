# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2

import streamlit as st
from logic import ExamLogic
import time

# הגדרות דף
st.set_page_config(page_title="מערכת בחינות - C-01", layout="wide")

# אתחול לוגיקה ב-Session State
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()

logic = st.session_state.logic

# --- פונקציות עזר ---
def handle_interaction():
    if not logic.timer_started:
        logic.timer_started = True

# --- סיידבר ---
st.sidebar.title("ניווט שאלות")
for i in range(1, 11):
    is_answered = i in logic.user_answers
    label = f"שאלה {i} {'✅' if is_answered else '❌'}"
    if st.sidebar.button(label, key=f"side_{i}"):
        handle_interaction()
        st.session_state.current_q = i

# --- אזור טיימר ---
timer_placeholder = st.empty()
if logic.timer_started:
    timer_placeholder.metric("זמן נותר", logic.get_time_string())

# --- גוף המבחן - תיקון הגרשיים ---
st.title('מבחן נדל"ן - C-01')

# --- כפתורי ניווט (הבא מימין, הקודם משמאל) ---
col_prev, col_spacer, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("< הקודם"):
        handle_interaction()
        st.rerun()

with col_next:
    if st.button("הבא >"):
        handle_interaction()
        st.rerun()

# עדכון אוטומטי של הטיימר
if logic.timer_started:
    time.sleep(1)
    st.rerun()
