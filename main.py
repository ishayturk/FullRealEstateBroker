import streamlit as st
import time
import logic

# גרסה: D-3000
def main():
    st.set_page_config(page_title="מערכת בחינות - D-3000", layout="wide")

    # אתחול סשן
    if 'user' not in st.session_state:
        st.session_state.user = "חיים חיים"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.exam_finished = False
        st.session_state.questions = logic.get_real_exam_data()

    st.header(f"בוחן: {st.session_state.user} | גרסה: D-3000")

    # מסך פתיחה
    if st.session_state.start_time is None:
        st.subheader("הנחיות לבדיקה")
        st.write("- 10 שאלות")
        st.write("- 2 דקות")
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # ניהול זמן
    remaining = logic.manage_exam_timer(st.session_state.start_time)
    st.sidebar.metric("זמן נותר", f"{int(remaining // 60):02d}:{int(remaining % 60):02d}")

    if remaining <= 0:
        st.session_state.exam_finished = True

    # תצוגת בחינה
    if not st.session_state.exam_finished:
        q_idx = st.session_state.current_q
        q = st.session_state.questions[q_idx]

        st.subheader(f"שאלה {q_idx + 1}")
        st.write(q["question"])
        
        choice = st.radio("בחר תשובה:", q["options"], index=None, key=f"q_{q_idx}")
        if choice:
            st.session_state.answers[q_idx] = choice

        # ניווט
        col1, col2 = st.columns(2)
        with col1:
            if q_idx > 0:
                if st.button("הקודם"):
                    st.session_state.current_q -= 1
                    st.rerun()
        with col2:
            # אכיפת לוגיקת ניווט C-01
            can_next = logic.can_move_next(q_idx, st.session_state.answers)
            if q_idx < len(st.session_state.questions) - 1:
                if st.button("הבא", disabled=not can_next):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה", disabled=not can_next):
                    st.session_state.exam_finished = True
                    st.rerun()
    
    # משוב
    else:
        score, feedback = logic.process_results(st.session_state.questions, st.session_state.answers)
        st.success(f"הבחינה הסתיימה! ציון: {score} מתוך 10")
        
        for item in feedback:
            with st.expander(f"שאלה {item['id']} - {item['status']}"):
                if item['status'] == "V":
                    st.write("V")
                else:
                    st.write(f"התשובה שלך: {item['user_ans']}")
                    st.write("") # שורת רווח לפי C-01
                    st.write(f"**התשובה הנכונה:** {item['correct_ans']}")

if __name__ == "__main__":
    main()
