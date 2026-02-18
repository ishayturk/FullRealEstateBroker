import streamlit as st
import time
import logic

# גרסה: D-3000
def main():
    # הגדרת יישור לימין (RTL) לכל האפליקציה
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            div[role="radiogroup"] { direction: rtl; text-align: right; }
            div.stButton > button { width: 100%; }
        </style>
    """, unsafe_allow_stdio=True)

    if 'questions' not in st.session_state:
        st.session_state.questions = logic.get_real_exam_data()
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.exam_finished = False

    # מסך פתיחה (Lobby)
    if st.session_state.start_time is None:
        st.subheader("מבחן תיווך - בדיקת מערכת")
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # טיימר ב-Sidebar
    remaining = logic.manage_exam_timer(st.session_state.start_time)
    mins, secs = divmod(int(remaining), 60)
    st.sidebar.metric("זמן נותר", f"{mins:02d}:{secs:02d}")

    if remaining <= 0 and not st.session_state.exam_finished:
        st.session_state.exam_finished = True
        st.rerun()

    # גוף הבחינה
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
    
    # משוב
    else:
        score, feedback = logic.process_results(st.session_state.questions, st.session_state.answers)
        st.success(f"הסתיים. ציון: {score} מתוך {len(st.session_state.questions)}")
        
        for item in feedback:
            with st.expander(f"שאלה {item['id']} - {item['status']}", expanded=(item['status'] == "X")):
                if item['status'] == "V":
                    st.write("V")
                else:
                    st.write(f"התשובה שלך: {item['user_ans']}")
                    st.write("") # שורת רווח לפי C-01
                    st.write(f"**התשובה הנכונה:** {item['correct_ans']}")

if __name__ == "__main__":
    main()
