# Version: C-05 | ID: C-01
import streamlit as st
import time

def show_instructions():
    st.title("📄 הוראות לבחינה")
    st.markdown("### הנחיות:\n* **מספר שאלות:** 25\n* **זמן:** 3 דקות\n* **שיטה:** טעינה מדורגת (Lazy Loading)")
    if st.button("התחל בחינה"):
        st.session_state.start_time = time.time()
        st.session_state.step = 'exam'
        st.rerun()

def render_navigation(total_loaded, is_mobile):
    if is_mobile:
        return st.sidebar.radio("שאלה:", range(1, total_loaded + 1), horizontal=True)
    return st.sidebar.radio("דלג לשאלה:", range(1, total_loaded + 1))

def show_results_summary(user_answers, exam_data):
    st.title("📊 סיכום תוצאות")
    score = 0
    for i, q in enumerate(exam_data):
        user_ans = user_answers.get(i, "לא נענתה")
        correct_ans = str(q['תשובה_נכונה']).strip()
        if str(user_ans).strip() == correct_ans:
            score += 1
            st.success(f"שאלה {i+1}: נכון ✅")
        else:
            st.error(f"שאלה {i+1}: טעות ❌ (תשובה נכונה: {correct_ans})")
    st.metric("ציון סופי", f"{int((score/len(exam_data))*100)}/100")
