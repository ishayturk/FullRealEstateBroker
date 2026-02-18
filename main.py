import streamlit as st
import time
import logic

# גרסה: D-3000 | עוגן לוגי: C-01
def init_exam():
    """איפוס מלא של נתוני הבחינה בסשן"""
    st.session_state.user = "חיים חיים"
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.start_time = None
    st.session_state.exam_finished = False
    st.session_state.questions = logic.get_real_exam_data()

def main():
    # הגדרות יישור לימין (RTL) ועיצוב
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            h1, h2, h3, p, span, label { text-align: right !important; direction: rtl !important; }
            div[role="radiogroup"] { direction: rtl; text-align: right; }
            .timer-box { 
                padding: 10px; border-radius: 5px; background: #fee; 
                color: #e74c3c; font-weight: bold; text-align: center; 
                font-size: 24px; border: 1px solid #e74c3c; margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # בדיקה אם צריך לאתחל את הסשן
    if 'questions' not in st.session_state:
        init_exam()

    # מסך פתיחה (Lobby)
    if st.session_state.start_time is None:
        st.header("מבחן תיווך - בדיקת מערכת")
        st.info("מבנה הבחינה: 10 שאלות | זמן: 2 דקות")
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # ניהול זמן
    remaining = logic.manage_exam_timer(st.session_state.start_time)
    
    # הצגת טיימר בפריים הראשי
    if not st.session_state.exam_finished:
        mins, secs = divmod(int(remaining), 60)
        st.markdown(f'<div class="timer-box">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # בדיקת סיום זמן
    if remaining <= 0 and not st.session_state.exam_finished:
        st.session_state.exam_finished = True
        st.rerun()

    # גוף הבחינה
    if not st.session_state.exam_finished:
        q_idx = st.session_state.current_q
        q = st.session_state.questions[q_idx]

        st.subheader(f"שאלה {q_idx + 1}")
        st.markdown(f"**{q['question']}**")
        
        # בחירת תשובה
        choice = st.radio(
            "בחר תשובה:", 
            q["options"], 
            index=q["options"].index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
            key=f"q_{q_idx}",
            label_visibility="collapsed"
        )
        
        if choice:
            st.session_state.answers[q_idx] = choice

        # ניווט
        col1, col2 = st.columns(2)
        with col2: # כפתור קודם בימין
            if q_idx > 0:
                if st.button("שאלה קודמת"):
                    st.session_state.current_q -= 1
                    st.rerun()
        with col1: # כפתור הבא בשמאל
            can_next = logic.can_move_next(q_idx, st.session_state.answers)
            if q_idx < len(st.session_state.questions) - 1:
                if st.button("שאלה הבאה", disabled=not can_next):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה", disabled=not can_next):
                    st.session_state.exam_finished = True
                    st.rerun()

        # ריענון אוטומטי של הטיימר
        time.sleep(1)
        st.rerun()
    
    # מסך משוב (Feedback)
    else:
        score, feedback = logic.process_results(st.session_state.questions, st.session_state.answers)
        st.header(f"{st.session_state.user} :: תוצאות בחינה רשם המתווכים")
        st.success(f"ציון סופי: {score} מתוך {len(st.session_state.questions)}")
        
        for item in feedback:
            with st.expander(f"שאלה {item['id']} - {item['status']}", expanded=(item['status'] == "X")):
                if item['status'] == "V":
                    st.write("V")
                else:
                    st.write(f"התשובה שלך: {item['user_ans']}")
                    st.write("") # שורת רווח לפי C-01
                    st.write(f"**התשובה הנכונה:** {item['correct_ans']}")
        
        if st.button("מבחן חדש (איפוס)"):
            del st.session_state.questions
            st.rerun()

if __name__ == "__main__":
    main()
