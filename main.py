# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2

import streamlit as st
import time

# הגדרת דף - חובה כפקודה ראשונה
st.set_page_config(page_title='מבחן נדל"ן - C-01', layout="wide")

# ניהול מצב האפליקציה (Session State)
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = 1
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

def start_timer():
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

# כותרת
st.title('מערכת בחינות נדל"ן - C-01')

# סיידבר - ניווט שאלות עם אינדיקציית מענה
st.sidebar.header("ניווט שאלות")
for i in range(1, 11):
    answered = i in st.session_state.user_answers
    status_icon = "✅" if answered else "❌"
    if st.sidebar.button(f"שאלה {i} {status_icon}", key=f"sq_{i}"):
        start_timer()
        st.session_state.current_q = i
        st.rerun()

# תצוגת טיימר (קפוא עד לחיצה ראשונה)
timer_placeholder = st.empty()
if st.session_state.start_time:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 7200 - elapsed)
    h, m = divmod(remaining // 60, 60)
    s = remaining % 60
    timer_placeholder.metric("זמן נותר", f"{h:02}:{m:02}:{s:02}")
else:
    timer_placeholder.metric("זמן נותר", "02:00:00 (קפוא)")

# אזור השאלה
st.subheader(f"שאלה {st.session_state.current_q}")
st.write("---")

# כפתורי ניווט: [הקודם] משמאל, [הבא] מימין
col_prev, col_spacer, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("< הקודם", use_container_width=True):
        start_timer()
        if st.session_state.current_q > 1:
            st.session_state.current_q -= 1
            st.rerun()

with col_next:
    if st.button("הבא >", use_container_width=True):
        start_timer()
        if st.session_state.current_q < 10:
            st.session_state.current_q += 1
            st.rerun()

# רענון אוטומטי לטיימר פעיל
if st.session_state.start_time:
    time.sleep(1)
    st.rerun()
