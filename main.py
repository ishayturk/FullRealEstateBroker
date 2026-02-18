import streamlit as st
import time
import logic

# גרסה: D-3000
def main():
    # הזרקת CSS ליישור לימין (RTL)
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            div[role="radiogroup"] { direction: rtl; text-align: right; }
        </style>
    """, unsafe_allow_html=True)

    if 'user' not in st.session_state:
        st.session_state.user = "חיים חיים"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.exam_finished = False
        st.session_state.questions = logic.get_real_exam_data()

    # שלב 1: מסך פתיחה
    if st.session_state.start_time is None:
        st.subheader("מבחן תיווך - בדיקת מערכת")
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # שלב 2: ניהול זמן
    remaining = logic.manage_exam_timer(st.session_state.start_time)
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("זמן נותר", f"{mins:02d}:{secs:02d}")

    if remaining <= 0 and not st.session_state.exam_finished:
        st.session_state.exam_finished = True
        st.rerun()

    # שלב 3: הצגת השאלות
    if not st.session_state.exam_finished:
        q_idx = st.session_state.current_q
        q = st.session_state.questions[q_idx]

        st.subheader(f"שאלה {q_idx + 1}")
        st.write(q["question"])
        
        choice = st.radio("בחר תשובה:", q["options"], 
                          index=q["options"].index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
                          key=f"q_{q_idx}")
        
        if choice:
            st.session_state.answers[q_idx] = choice

        col1, col2 = st.columns(2)
        with col2:
            if q_idx > 0:
                if st.button("הקודם"):
                    st.session_state.current_q -= 1
                    st.rerun()
        with col1:
            can_next = logic.can_move_next(q_idx, st.session_state.answers)
            if q_idx < len(st.session_state.questions) - 1:
                if st.button("הבא", disabled=not can_next):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה", disabled=not can_next):
                    st.session_state.exam_finished = True
                    st.rerun()
    
    # שלב 4: משוב (כאן העדכון לבקשתך)
    else:
        score, feedback = logic.process_results(st.session_state.questions, st.session_state.answers)
        
        # כותרת מעודכנת
        st.header(f"{st.session_state.user} :: תוצאות בחינה רשם המתווכים")
        st.success(f"ציון סופי: {score} מתוך {len(st.session_state.questions)}")
        
        for item in feedback:
            with st.expander(f"שאלה {item['id']} - {item['status']}", expanded=(item['status'] == "X")):
                if item['status'] == "V":
                    st.write("V")
                else:
                    st.write(f"התשובה שלך: {item['user_ans']}")
                    st.write("") # רווח לפי C-01
                    st.write(f"**התשובה הנכונה:** {item['correct_ans']}")

if __name__ == "__main__":
    main()
