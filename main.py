# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2

import streamlit as st
from logic import ExamLogic
import time

# אתחול רכיבים
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

logic = st.session_state.logic

def trigger_start():
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

# תצוגה
st.title('מבחן נדל"ן - C-01')

# סיידבר - ניווט וצביעה
st.sidebar.header("ניווט שאלות")
for i in range(1, 11):
    answered = i in st.session_state.user_answers
    # צביעת רקע ב-Streamlit מתבצעת ע"י כפתורים/אינדיקטורים
    label = f"שאלה {i} {'✅' if answered else '❌'}"
    if st.sidebar.button(label, key=f"q_{i}"):
        trigger_start()
        st.session_state.current_question = i

# אזור טיימר
timer_place = st.empty()
if st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, logic.total_seconds - int(elapsed))
    timer_place.metric("זמן נותר", logic.get_time_string(remaining))
else:
    timer_place.metric("זמן נותר", "02:00:00 (קפוא)")

# ניווט תחתון - [הקודם] משמאל, [הבא] מימין
st.write("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.button("< הקודם"):
        trigger_start()
with c3:
    if st.button("הבא >"):
        trigger_start()

# מנגנון רענון לטיימר
if st.session_state.start_time:
    time.sleep(1)
    st.rerun()
