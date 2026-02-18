import streamlit as st
import time
import logic

# גרסה: D-3000 | עוגן: C-01
def main():
    # הזרקת CSS לתיקון יישור לימין (RTL) ועיצוב הטיימר
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            /* יישור כותרות ושאלות */
            h1, h2, h3, p, span, label { text-align: right !important; direction: rtl !important; }
            /* יישור רכיב התשובות (Radio) */
            div[role="radiogroup"] { direction: rtl; text-align: right; margin-right: 0; }
            div[data-testid="stMarkdownContainer"] > p { text-align: right; }
            /* עיצוב טיימר בולט במרכז */
            .timer-box { 
                padding: 10px; border-radius: 5px; background: #fee; 
                color: #e74c3c; font-weight: bold; text-align: center; 
                font-size: 24px; border: 1px solid #e74c3c; margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    if 'user' not in st.session_state:
        st.session_state.user = "חיים חיים"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.start_time = None
        st.session_state.exam_finished = False
        st.session_state.questions = logic.get_real_exam_data()

    # מסך פתיחה
    if st.session_state.start_time is None:
        st.header("מבחן תיווך - בדיקת מערכת")
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # ניהול זמן בפריים הראשי עם ריענון אוטומטי
    remaining = logic.manage_exam_timer(st.session_state.start_time)
    mins, secs = divmod(int(remaining), 60)
    
    # הצגת הטיימר בפריים הראשי
    timer_placeholder = st.empty()
    timer_placeholder.markdown(f'<div class="timer-box">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    if remaining <= 0 and not st.session_state.exam_finished:
        st.session_state.exam_finished = True
        st.rerun()

    # גוף הבחינה
    if not st.session_state.exam_finished:
        q_idx = st.session_state.current_q
        q = st.session_state.questions[q_idx]

        st.subheader(f"שאלה {q_idx + 1}")
        st.markdown(f"**{q['question']}**")
        
        # תצוגת תשובות - מיושר לימין
        choice = st.radio(
            "בחר תשובה:", 
            q["options"], 
            index=q["options"].index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
            key=f"q_{q_idx}",
            label_visibility="collapsed" # מסתירים את הלייבל המובנה כדי למנוע כפילות
        )
        
        if choice:
            st.session_state.answers[q_idx] = choice

        # כפתורי ניווט (הפוך בגלל ה-RTL: הקודם מימין, הבא משמאל)
        col1, col2 = st.columns(2)
        with col1:
            if q_idx > 0:
                if st.button("שאלה קודמת"):
                    st.session_state.current_q -= 1
                    st.rerun()
        with col2:
            can_next = logic.can_move_next(q_idx, st.session_state.answers)
            if q_idx < len(st.session_state.questions) - 1:
                if st.button("שאלה הבאה", disabled=not can_next):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה", disabled=not can_next):
                    st.session_state.exam_finished = True
                    st.rerun()

        # ריענון אוטומטי של הטיימר (כל שנייה)
        if remaining > 0:
            time.sleep(1)
            st.rerun()
    
    # משוב
    else:
        score, feedback = logic.process_results(st.session_state.questions, st.session_state.answers)
        st.header(f"{st.session_state.user} :: תוצאות בחינה רשם המתווכים")
        st.success(f"ציון סופי: {score} מתוך {len(st.session_state.questions)}")
        
        for item in feedback:
            with st.expander(f"שאלה {item['id']} - {item['status']}", expanded=(item['status'] == "X")):
                if item['status'] == "V":
                    st.markdown('<p style="color:green; font-weight:bold;">תשובה נכונה! V</p>', unsafe_allow_html=True)
                else:
                    st.write(f"התשובה שלך: {item['user_ans']}")
                    st.write("") 
                    st.write(f"**התשובה הנכונה:** {item['correct_ans']}")

if __name__ == "__main__":
    main()
