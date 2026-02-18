import streamlit as st
import time
from logic import ExamManager

# גרסה: D-3000
def main():
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            [data-testid="stSidebar"] { direction: rtl; text-align: right; }
            .timer-box { 
                padding: 10px; border-radius: 8px; background: #fff5f5; 
                color: #d9534f; font-weight: bold; text-align: center; 
                font-size: 28px; border: 1px solid #d9534f; margin-bottom: 20px;
            }
            .stButton > button { width: 100%; }
        </style>
    """, unsafe_allow_html=True)

    if 'exam' not in st.session_state:
        st.session_state.exam = ExamManager()
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.finished = False

    # --- דף המעבר (Lobby) ---
    if st.session_state.start_time is None:
        st.header("הכנה לבחינת רשם המתווכים")
        st.subheader("שלום, " + st.session_state.exam.user_name)
        
        st.info("""
        **הנחיות לבחינה:**
        1. הבחינה כוללת 10 שאלות אמיתיות.
        2. עליך לענות על שאלה כדי להתקדם לבאה (ניתן לחזור אחורה).
        3. לרשותך 120 שניות (2 דקות) לבחינה כולה.
        """)
        
        # צ'ק-בוקסים לאישור
        agree1 = st.checkbox("אני מבין שהניווט קדימה מותנה במתן תשובה.")
        agree2 = st.checkbox("אני מאשר שהטיימר יתחיל ברגע לחיצה על הכפתור.")
        
        if st.button("התחל בחינה עכשיו", disabled=not (agree1 and agree2)):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # --- ניווט ב-Sidebar (מספרים ב-Grid) ---
    if not st.session_state.finished:
        st.sidebar.subheader("ניווט מהיר")
        cols = st.sidebar.columns(3)
        for i in range(len(st.session_state.exam.questions)):
            with cols[i % 3]:
                # חסימת ניווט קדימה לפי C-01
                is_disabled = i > len(st.session_state.answers)
                if st.button(f"{i+1}", key=f"nav_{i}", disabled=is_disabled):
                    st.session_state.current_q = i
                    st.rerun()

    # --- גוף המבחן ---
    remaining = st.session_state.exam.get_remaining_time(st.session_state.start_time)
    
    if not st.session_state.finished:
        # טיימר במרכז
        mins, secs = divmod(int(remaining), 60)
        st.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
        if remaining <= 0:
            st.session_state.finished = True
            st.rerun()

        # תצוגת שאלה
        idx = st.session_state.current_q
        q = st.session_state.exam.questions[idx]
        st.subheader(f"שאלה {idx + 1}")
        st.markdown(f"**{q['question']}**")
        
        choice = st.radio("בחר תשובה:", q["options"], 
                          index=q["options"].index(st.session_state.answers[idx]) if idx in st.session_state.answers else None,
                          key=f"q_{idx}", label_visibility="collapsed")
        if choice:
            st.session_state.answers[idx] = choice

        # כפתורי ניווט
        st.write("---")
        c1, c2 = st.columns(2)
        with c2:
            if idx > 0 and st.button("⬅️ קודמת"):
                st.session_state.current_q -= 1
                st.rerun()
        with c1:
            if idx < 9:
                if st.button("הבאה ➡️", disabled=idx not in st.session_state.answers):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה 🏁", disabled=idx not in st.session_state.answers):
                    st.session_state.finished = True
                    st.rerun()

        time.sleep(1)
        st.rerun()

    # --- משוב ---
    else:
        score, feedback = st.session_state.exam.process_results(st.session_state.answers)
        st.header(f"{st.session_state.exam.user_name} :: תוצאות בחינה רשם המתווכים")
        st.success(f"ציון סופי: {score} מתוך 10")
        for f in feedback:
            with st.expander(f"שאלה {f['id']} - {f['status']}", expanded=(f['status'] == "X")):
                if f['status'] == "V": st.write("V")
                else:
                    st.write(f"תשובתך: {f['user_ans']}")
                    st.write("")
                    st.write(f"**התשובה הנכונה:** {f['correct_ans']}")
        if st.button("מבחן חדש"):
            del st.session_state.exam
            st.rerun()

if __name__ == "__main__":
    main()
