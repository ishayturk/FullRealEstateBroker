# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V04 | Date: 21/02/2026 | 23:15
import streamlit as st
import logic

# הגדרות עמוד
st.set_page_config(page_title="מתווך בקליק", layout="wide")

# אתחול מצב עמוד
if "page" not in st.session_state:
    st.session_state.page = "explanation"

# CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        direction: rtl;
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
        border-bottom: 1px solid #ddd;
    }
    div[role="radiogroup"] {
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# --- סטריפ עליון קבוע (Header) ---
st.write("") # שורה אחת מתחת לקצה
h_col1, h_col2, h_col3 = st.columns([1, 2, 1])
with h_col1:
    st.button("חזרה", key="nav_back_btn")
with h_col2:
    st.markdown("<p style='text-align: center;'>ישראל ישראלי</p>", unsafe_allow_html=True)
with h_col3:
    st.markdown("<p style='text-align: right;'>מתווך בקליק</p>", unsafe_allow_html=True)

st.divider()

# אתחול לוגיקה
logic.initialize_exam()

# --- ניהול דפים ---

if st.session_state.page == "explanation":
    # שחזור דף ההסבר המקורי ללא שינוי
    st.markdown("<h1 style='text-align: center;'>ברוכים הבאים לבחינה</h1>", unsafe_allow_html=True)
    st.write("---")
    st.write("כאן מופיעות הוראות הבחינה המקוריות כפי שהיו בגרסה 1218-G2.")
    st.write("1. משך הבחינה 90 דקות.")
    st.write("2. יש לענות על 25 שאלות.")
    st.write("3. בכל שאלה יש לבחור תשובה אחת מתוך ארבע.")
    
    st.write("")
    # השורה של הצ'קבוקס והכפתור כפי שהוגדרה במקור
    c1, c2 = st.columns([1, 1])
    with c1:
        agree = st.checkbox("קראתי והבנתי את ההוראות")
    with c2:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.page = "exam"
            st.session_state.start_time = logic.time.time()
            # ייצור שאלה 2 ברגע הלחיצה
            logic.generate_question(2)
            st.rerun()

elif st.session_state.page == "exam":
    if logic.check_exam_status():
        st.session_state.page = "time_up"
        st.rerun()

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

    q_num = st.session_state.current_q
    q_data = st.session_state.exam_data.get(q_num)

    if q_data:
        st.subheader(f"שאלה {q_num}")
        st.write(q_data["question"])
        
        choice = st.radio("בחר תשובה:", q_data["options"], 
                          index=st.session_state.answers_user.get(q_num), 
                          key=f"radio_q_{q_num}")
        
        if choice:
            st.session_state.answers_user[q_num] = q_data["options"].index(choice)

        st.divider()
        nav1, nav2, nav3 = st.columns(3)
        with nav1:
            if st.button("שאלה קודמת", disabled=(q_num == 1)):
                logic.handle_navigation("prev")
                st.rerun()
        with nav2:
            is_next_disabled = (q_num not in st.session_state.answers_user) or (q_num == 25)
            if st.button("שאלה הבאה", disabled=is_next_disabled):
                logic.handle_navigation("next")
                st.rerun()
        with nav3:
            if 25 in st.session_state.answers_user:
                if st.button("סיים בחינה"):
                    st.session_state.page = "summary"
                    st.rerun()

elif st.session_state.page == "time_up":
    st.header("הזמן לבחינה הסתיים")
    if st.button("לסיום הבחינה לחץ: סיים בחינה"):
        st.session_state.page = "summary"
        st.rerun()

elif st.session_state.page == "summary":
    st.header("תוצאות הבחינה")
    st.write("דף משוב בבנייה...")

# סוף קובץ
