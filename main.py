import streamlit as st
import time
from logic import ExamManager

# גרסה: D-3000
def main():
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            h1, h2, h3, p, span, label, div { text-align: right !important; direction: rtl !important; }
            div[role="radiogroup"] { direction: rtl; text-align: right; }
            .timer-box { 
                padding: 10px; border-radius: 5px; background: #fff5f5; 
                color: #d9534f; font-weight: bold; text-align: center; 
                font-size: 24px; border: 1px solid #d9534f; margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    if 'exam' not in st.session_state:
        st.session_state.exam = ExamManager()
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.finished = False

    # מסך פתיחה
    if st.session_state.start_time is None:
        st.header("מבחן רשם המתווכים - פתיחה")
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # טיימר בפריים הראשי (לא בסידבר)
    remaining = st.session_state.exam.get_remaining_time(st.session_state.start_time)
    if not st.session_state.finished:
        mins, secs = divmod(int(remaining), 60)
        st.markdown(f'<div class="timer-box">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        if remaining <= 0:
            st.session_state.finished = True
            st.rerun()

    # --- ניווט ב-Sidebar ---
    st.sidebar.title("ניווט שאלות")
    for i in range(len(st.session_state.exam.questions)):
        # חסימת ניווט קדימה לשאלות שלא הגענו אליהן/ענינו עליהן
        is_disabled = i > len(st.session_state.answers)
        if st.sidebar.button(f"שאלה {i+1}", key=f"nav_{i}", disabled=is_disabled):
            st.session_state.current_q = i
            st.rerun()

    # --- גוף השאלה ---
    if not st.session_state.finished:
        idx = st.session_state.current_q
        q = st.session_state.exam.questions[idx]
        st.subheader(f"שאלה {idx + 1}")
        st.write(q["question"])
        
        choice = st.radio("תשובה:", q["options"], 
                          index=q["options"].index(st.session_state.answers[idx]) if idx in st.session_state.answers else None,
                          key=f"q_{idx}", label_visibility="collapsed")
        if choice:
            st.session_state.answers[idx] = choice

        # כפתורי ניווט תחתונים
        col1, col2 = st.columns(2)
        with col2:
            if idx > 0 and st.button("⬅️ שאלה קודמת"):
                st.session_state.current_q -= 1
                st.rerun()
        with col1:
            if idx < 9:
                if st.button("שאלה הבאה ➡️", disabled=idx not in st.session_state.answers):
                    st.session_state.current_q += 1
                    st.rerun()
            elif st.button("סיים בחינה 🏁", disabled=idx not in st.session_state.answers):
                st.session_state.finished = True
                st.rerun()

        time.sleep(1)
        st.rerun()

    # --- משוב סופי ---
    else:
        score, feedback = st.session_state.exam.process_results(st.session_state.answers)
        st.header(f"{st.session_state.exam.user_name} :: תוצאות בחינה רשם המתווכים")
        st.success(f"ציון: {score} מתוך 10")
        for f in feedback:
            with st.expander(f"שאלה {f['id']} - {f['status']}", expanded=(f['status'] == "X")):
                if f['status'] == "V": st.write("V")
                else:
                    st.write(f"תשובתך: {f['user_ans']}")
                    st.write("")
                    st.write(f"**נכונה:** {f['correct_ans']}")
        if st.button("מבחן חדש"):
            del st.session_state.exam
            st.rerun()

if __name__ == "__main__":
    main()
