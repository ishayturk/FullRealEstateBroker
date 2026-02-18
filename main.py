import streamlit as st
import time
from logic import ExamManager

# גרסה: D-3000
def reset_exam_state():
    """פונקציה לניקוי מוחלט של הסשן - למניעת כניסה ישר לתוצאות"""
    st.session_state.exam = ExamManager()
    st.session_state.current_q = 0
    st.session_state.answers = {}
    st.session_state.start_time = None
    st.session_state.finished = False

def main():
    # עיצוב ויישור לימין
    st.markdown("""
        <style>
            .stApp { direction: rtl; text-align: right; }
            [data-testid="stSidebar"] { direction: rtl; text-align: right; }
            .timer-box { 
                padding: 10px; border-radius: 8px; background: #fff5f5; 
                color: #d9534f; font-weight: bold; text-align: center; 
                font-size: 28px; border: 1px solid #d9534f; margin-bottom: 20px;
            }
            div[role="radiogroup"] { direction: rtl; text-align: right; }
            .stButton > button { width: 100%; }
        </style>
    """, unsafe_allow_html=True)

    # אתחול סשן ראשוני בלבד
    if 'exam' not in st.session_state:
        reset_exam_state()

    # --- 1. דף המעבר (Lobby) ---
    if st.session_state.start_time is None:
        st.header("ברוך הבא למבחן רשם המתווכים")
        st.subheader(f"נבחן: {st.session_state.exam.user_name}")
        
        st.write("### הנחיות לפני התחלה:")
        st.write("* 10 שאלות אמיתיות ממאגר רשם המתווכים.")
        st.write("* זמן מוקצב: **2 דקות** (120 שניות).")
        st.write("* לא ניתן לדלג קדימה על שאלה מבלי לענות עליה.")
        
        st.markdown("---")
        # צ'ק-בוקסים מחייבים
        c1 = st.checkbox("קראתי את ההנחיות ואני מוכן להתחיל.")
        c2 = st.checkbox("אני מבין שהטיימר יתחיל לפעול מיד עם הלחיצה.")
        
        if st.button("🚀 התחל בחינה", disabled=not (c1 and c2)):
            st.session_state.start_time = time.time()
            st.rerun()
        return

    # --- 2. ניווט ב-Sidebar (במהלך הבחינה בלבד) ---
    if not st.session_state.finished:
        st.sidebar.subheader("ניווט שאלות")
        cols = st.sidebar.columns(3) # 3 שאלות בשורה
        for i in range(len(st.session_state.exam.questions)):
            with cols[i % 3]:
                # חסימת ניווט קדימה - C-01
                is_disabled = i > len(st.session_state.answers)
                if st.button(f"{i+1}", key=f"nav_{i}", disabled=is_disabled):
                    st.session_state.current_q = i
                    st.rerun()

    # --- 3. גוף הבחינה והטיימר ---
    remaining = st.session_state.exam.get_remaining_time(st.session_state.start_time)
    
    if not st.session_state.finished:
        # הצגת טיימר במרכז
        mins, secs = divmod(int(remaining), 60)
        st.markdown(f'<div class="timer-box">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
        if remaining <= 0:
            st.session_state.finished = True
            st.rerun()

        # הצגת השאלה הנוכחית
        idx = st.session_state.current_q
        q = st.session_state.exam.questions[idx]
        st.subheader(f"שאלה {idx + 1}")
        st.markdown(f"**{q['question']}**")
        
        choice = st.radio("תשובות:", q["options"], 
                          index=q["options"].index(st.session_state.answers[idx]) if idx in st.session_state.answers else None,
                          key=f"q_{idx}", label_visibility="collapsed")
        if choice:
            st.session_state.answers[idx] = choice

        # כפתורי ניווט תחתונים
        st.divider()
        col_r, col_l = st.columns(2)
        with col_r:
            if idx > 0 and st.button("⬅️ שאלה קודמת"):
                st.session_state.current_q -= 1
                st.rerun()
        with col_l:
            if idx < 9:
                if st.button("שאלה הבאה ➡️", disabled=idx not in st.session_state.answers):
                    st.session_state.current_q += 1
                    st.rerun()
            else:
                if st.button("סיים וקבל תוצאות 🏁", disabled=idx not in st.session_state.answers):
                    st.session_state.finished = True
                    st.rerun()

        time.sleep(1)
        st.rerun()

    # --- 4. מסך תוצאות ---
    else:
        score, feedback = st.session_state.exam.process_results(st.session_state.answers)
        st.header(f"{st.session_state.exam.user_name} :: תוצאות בחינה רשם המתווכים")
        st.success(f"סיימת! הציון שלך הוא: {score} מתוך 10")
        
        for f in feedback:
            status_color = "green" if f['status'] == "V" else "red"
            with st.expander(f"שאלה {f['id']} - {f['status']}", expanded=(f['status'] == "X")):
                if f['status'] == "V":
                    st.markdown(f'<p style="color:{status_color}">תשובה נכונה! V</p>', unsafe_allow_html=True)
                else:
                    st.write(f"התשובה שלך: {f['user_ans']}")
                    st.write("") # רווח לפי C-01
                    st.write(f"**התשובה הנכונה:** {f['correct_ans']}")
        
        if st.button("🔄 למבחן חדש (איפוס)"):
            reset_exam_state()
            st.rerun()

if __name__ == "__main__":
    main()
