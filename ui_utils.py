# Version: C-06.1 | ID: C-01
import streamlit as st
import time

def show_instructions():
    st.write("בחינה: 25 שאלות | זמן: 3 דקות")
    if st.button("התחל"):
        st.session_state.start_time = time.time()
        st.session_state.step = 'exam'
        st.rerun()

def render_navigation(total_loaded, is_mobile):
    return st.sidebar.radio("שאלה:", range(1, total_loaded + 1), horizontal=is_mobile)

def show_results_summary(user_answers, exam_data):
    score = 0
    for i, q in enumerate(exam_data):
        user_ans = user_answers.get(i, "")
        correct = str(q['תשובה_נכונה']).strip()
        if str(user_ans).strip() == correct:
            score += 1
            st.success(f"{i+1}: נכון")
        else:
            st.error(f"{i+1}: טעות (נכון: {correct})")
    st.metric("ציון", f"{int((score/len(exam_data))*100)}/100")
