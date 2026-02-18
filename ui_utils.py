# Version: C-02
# Based on Anchor: 1218-G2
# Description: UI components with timer-start logic and full feedback display.

import streamlit as st
import time

def show_instructions():
    """מסך פתיחה עם המלל המדויק והתניית התחלת המבחן"""
    st.title("📄 הוראות לבחינה")
    st.markdown("""
    ### הנחיות:
    * **מספר שאלות:** 25.
    * **זמן בחינה:** 3 דקות (לצורך הבדיקה).
    * **ניווט:** ניתן לעבור בין שאלות ולשנות תשובות בכל עת.
    
    ---
    **שימו לב: המבחן יתחיל ברגע שתלחץ/י על כפתור התחל בחינה**
    """)
    
    if st.button("התחל בחינה"):
        st.session_state.start_time = time.time()
        st.session_state.step = 'exam'
        st.rerun()

def render_navigation(total_loaded, is_mobile):
    """ניהול ניווט בשאלות שנטענו"""
    if is_mobile:
        with st.sidebar.expander("🔍 ניווט שאלות", expanded=False):
            return st.radio("בחר שאלה:", range(1, total_loaded + 1), horizontal=True)
    st.sidebar.title("ניווט")
    return st.sidebar.radio("דלג לשאלה:", range(1, total_loaded + 1))

def show_results_summary(user_answers, exam_data):
    """הצגת תוצאות עם מלל מלא של התשובות"""
    st.title("📊 סיכום תוצאות")
    score = 0
    
    for i, q in enumerate(exam_data):
        user_ans = user_answers.get(i, "לא נענתה")
        correct_ans = str(q['תשובה_נכונה']).strip()
        
        if str(user_ans).strip() == correct_ans:
            score += 1
            st.success(f"שאלה {i+1}: נכון ✅")
        else:
            st.error(f"שאלה {i+1}: טעות ❌")
            st.write(f"**התשובה שלך:** {user_ans}")
            st.write(f"**התשובה הנכונה:** {correct_ans}")
        st.divider()
    
    final_grade = int((score / len(exam_data)) * 100)
    st.metric("ציון סופי", f"{final_grade}/100")
