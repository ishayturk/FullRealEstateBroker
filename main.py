# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V03 | Date: 21/02/2026 | 23:10
import streamlit as st
import logic

# הגדרות עמוד
st.set_page_config(page_title="מתווך בקליק", layout="wide")

# אתחול מצב עמוד (ברירת מחדל: דף הסבר)
if "page" not in st.session_state:
    st.session_state.page = "explanation"

# CSS לעיצוב הסטריפ והאלמנטים
st.markdown("""
    <style>
    .header-strip {
        padding: 10px 0px;
        border-bottom: 1px solid #ddd;
        margin-bottom: 20px;
    }
    .sticky-timer {
        position: fixed;
        top: 45px;
        right: 0;
        left: 0;
        background-color: #f0f2f6;
        text-align: center;
        padding: 5px;
        font-weight: bold;
        z-index: 1000;
    }
    div[role="radiogroup"] {
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# --- סטריפ עליון קבוע (Header) ---
# שורה אחת מתחת לקצה העליון כפי שהוגדר
st.write("") 
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col1:
    if st.button("חזרה", key="back_btn"):
        pass # לוגיקת חזרה לתפריט חיצוני
with header_col2:
    st.markdown("<p style='text-align: center;'>ישראל ישראלי</p>", unsafe_allow_html=True)
with header_col3:
    st.markdown("<p style='text-align: right;'>לוגו: מתווך בקליק</p>", unsafe_allow_html=True)

st.divider()

# אתחול נתוני בחינה (מכין את שאלה 1 ברקע)
logic.initialize_exam()

# --- ניהול דפים ---

# 1. דף הסבר
if st.session_state.page == "explanation":
    st.title("הסבר על הבחינה")
    st.write("כאן מופיע מלל ההסבר כפי שהוגדר בעבר...")
    
    col_check, col_start = st.columns([1, 1])
    with col_check:
        agree = st.checkbox("קראתי והבנתי את ההוראות")
    with col_start:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.page = "exam"
            st.session_state.start_time = logic.time.time() # התחלת טיימר
            logic.handle_navigation("start") # טעינת שאלה 2
            st.rerun()

# 2. דף בחינה
elif st.session_state.page == "exam":
    if logic.check_exam_status():
        st.session_state.page = "time_up"
        st.rerun()

    # סיידבר ניווט
    with st.sidebar:
        st.markdown(f'<div class="sticky-timer">זמן נותר: {logic.get_timer_display()}</div>', unsafe_allow_html=True)
        st.write("---")
        st.write("ניווט שאלות:")
        for row in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                q_idx = row + i + 1
                if q_idx <= 25:
                    is_disabled = q_idx not in st.session_state.answers_user and q_idx != st.session_state.current_q
                    if col.button(f"{q_idx}", key=f"side_{q_idx}", disabled=is_disabled):
                        st.session_state.current_q = q_idx
                        st.rerun()

    # הצגת שאלה
    q_num = st.session_state.current_q
    q_data = st.session_state.exam_data.get(q_num)

    if q_data:
        st.subheader(f"שאלה {q_num}")
        st.write(q_data["question"])
        
        choice = st.radio("בחר תשובה:", q_data["options"], 
                          index=st.session_state.answers_user.get(q_num), 
                          key=f"q_{q_num}")
        
        if choice:
            st.session_state.answers_user[q_num] = q_data["options"].index(choice)

        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("שאלה קודמת", disabled=(q_num == 1)):
                logic.handle_navigation("prev")
                st.rerun()
        with c2:
            is_next_off = (q_num not in st.session_state.answers_user) or (q_num == 25)
            if st.button("שאלה הבאה", disabled=is_next_off):
                logic.handle_navigation("next")
                st.rerun()
        with c3:
            if 25 in st.session_state.answers_user:
                if st.button("סיים בחינה"):
                    st.session_state.page = "summary"
                    st.rerun()

# 3. דף סיום זמן
elif st.session_state.page == "time_up":
    st.header("הזמן לבחינה הסתיים")
    if st.button("לסיום הבחינה לחץ: סיים בחינה"):
        st.session_state.page = "summary"
        st.rerun()

# 4. דף משוב (סיכום)
elif st.session_state.page == "summary":
    st.header("תוצאות הבחינה")
    # כאן תבוא לוגיקת הציון וה-V/X
    st.write("דף משוב בבנייה...")

# סוף קובץ
