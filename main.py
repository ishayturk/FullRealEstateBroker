import streamlit as st
import time
from logic import ExamManager

# גרסה: D-3000
def main():
    # יישור לימין (RTL)
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            h1, h2, h3, p, span, label { text-align: right !important; }
            div[role="radiogroup"] { direction: rtl; text-align: right; }
            .timer-box { 
                padding: 15px; border-radius: 8px; background: #fff5f5; 
                color: #d9534f; font-weight: bold; text-align: center; 
                font-size: 28px; border: 2px solid #d9534f; margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # שימוש בבנאי (Constructor) דרך ה-session_state
    if 'exam' not in st.session_state:
        st.session_state.exam = ExamManager()
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.finished = False

    # 1. מסך התחלה
    if st.session_state.start_time is None:
        st.header("מערכת בחינות - רשם המתווכים")
        if st.button("התחל בחינה עכשיו"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # 2. ניהול והצגת הטיימר (החלק שחזר)
    remaining = st.session_state.exam.get_remaining_time(st.session_state.start_time)
    
    if not st.session_state.finished:
        mins, secs = divmod(int(remaining), 60)
        timer_placeholder = st.empty()
        timer_placeholder.markdown(f'<div class="timer-box">⏳ זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

        if remaining <= 0:
            st.session_state.finished = True
            st.rerun()

    # 3. גוף המבחן
    if not st.session_state.finished:
        idx = st.session_state.current_q
        q = st.session_state.exam.questions[idx]

        st.subheader(f"שאלה {idx + 1}")
        st.write(q["question"])
        
        choice = st.radio("תשובות:", q["options"], 
                          index=q["options"].index(st.session_state.answers[idx]) if idx in st.session_state.answers else None,
                          key=f"r_{idx}", label_visibility="collapsed")
        
        if choice:
            st.session_state.answers[idx] = choice

        # ניווט (חסימה לפי C-01)
        col1, col2 = st.columns(2)
        with col2:
            if idx > 0:
                if st.button("שאלה קודמת"):
                    st.session_state.current_q -= 1
                    st.rerun()
        with col1:
            can_next = st.session_state.exam.can_navigate_next(idx, st.session_state.answers)
            if idx < 9:
                if st.button("שאלה הבאה", disabled=not can_next):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה", disabled=not can_next):
                    st.session_state.finished = True
                    st.rerun()

        # ריענון אוטומטי של השעון
        time.sleep(1)
        st.rerun()

    # 4. משוב סופי
    else:
        score, feedback = st.session_state.exam.process_results(st.session_state.answers)
        st.header(f"{st.session_state.exam.user_name} :: תוצאות בחינה רשם המתווכים")
        st.success(f"הציון שלך: {score} מתוך 10")
        
        for f in feedback:
            with st.expander(f"שאלה {f['id']} - {f['status']}", expanded=(f['status'] == "X")):
                if f['status'] == "V":
                    st.write("V")
                else:
                    st.write(f"התשובה שלך: {f['user_ans']}")
                    st.write("") # רווח
                    st.write(f"**התשובה הנכונה:** {f['correct_ans']}")
        
        if st.button("מבחן חדש"):
            del st.session_state.exam
            st.rerun()

if __name__ == "__main__":
    main()
