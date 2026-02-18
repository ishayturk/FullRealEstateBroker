# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2
# DESCRIPTION: Streamlit UI conversion to fix ImportError (No Tkinter on Cloud)

import streamlit as st
from logic import ExamLogic
import time

# הגדרות דף
st.set_page_config(page_title="מערכת בחינות - C-01", layout="wide")

# אתחול לוגיקה ב-Session State כדי שלא תתאפס בכל ריצה
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()

logic = st.session_state.logic

# --- פונקציות עזר ---
def handle_interaction():
    if not logic.timer_started:
        logic.timer_started = True

# --- סיידבר (סימון שאלות שלא נענו) ---
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
    # הצגת זמן (ב-Streamlit הטיימר רץ קצת אחרת)
    timer_placeholder.metric("זמן נותר", logic.get_time_string())

# --- גוף המבחן ---
st.title("מבחן נדל"ן - C-01")

# --- כפתורי ניווט (הבא מימין, הקודם משמאל) ---
col_prev, col_spacer, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("< הקודם"):
        handle_interaction()
        # לוגיקה לקודם
        st.rerun()

with col_next:
    if st.button("הבא >"):
        handle_interaction()
        # לוגיקה להבא
        st.rerun()

# עדכון אוטומי של הטיימר אם הוא הופעל
if logic.timer_started:
    time.sleep(1)
    # כאן אפשר להוסיף לוגיקת הפחתת זמן ב-logic
    st.rerun()
