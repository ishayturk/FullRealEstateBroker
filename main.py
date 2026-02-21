# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V02 | Date: 22/02/2026 | 01:10
import streamlit as st
import logic

# הגדרות עמוד
st.set_page_config(page_title="מתווך בקליק - בחינה", layout="wide")

# CSS להצמדת הטיימר לראש הדף ועיצוב הרדיו-בטאן מימין לשמאל
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        direction: rtl;
    }
    .sticky-timer {
        position: fixed;
        top: 40px;
        right: 0;
        left: 0;
        background-color: #f0f2f6;
        text-align: center;
        padding: 5px;
        font-weight: bold;
        z-index: 1000;
        border-bottom: 1px solid #ddd;
    }
    .stRadio [data-testid="stWidgetLabel"] {
        text-align: right;
        direction: rtl;
    }
    div[role="radiogroup"] {
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# אתחול לוגיקה
logic.initialize_exam()

# --- סטריפ עליון קבוע (Header) ---
col_logo, col_name, col_back = st.columns([1, 2, 1])
with col_logo:
    st.write("לוגו: מתווך בקליק")
with col_name:
    st.write(f"שם המשתמש: ישראל ישראלי")
with col_back:
    if st.button("חזרה לתפריט"):
        st.write("מעבר לתפריט ראשי...")

st.divider()

# בדיקה אם הזמן נגמר
if logic.check_exam_status():
    st.header("הזמן לבחינה הסתיים")
    st.write("לסיום הבחינה לחץ:")
    if st.button("סיים בחינה"):
        st.session_state.page = "summary"
        st.rerun()
else:
    # --- תצוגת בחינה (Sidebar) ---
    with st.sidebar:
        st.markdown(f'<div class="sticky-timer">זמן נותר: {logic.get_timer_display()}</div>', unsafe_allow_html=True)
        st.write("---")
        st.write("ניווט שאלות:")
        
        # יצירת גריד של 4 כפתורים בשורה, משמאל לימין
        for row in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                q_idx = row + i + 1
                if q_idx <= 25:
                    # כפתור אקטיבי רק אם השאלה נענתה או שהיא הנוכחית
                    is_disabled = q_idx not in st.session_state.answers_user and q_idx != st.session_state.current_q
                    if col.button(f"{q_idx}", key=f"btn_{q_idx}", disabled=is_disabled):
                        st.session_state.current_q = q_idx
                        st.rerun()

    # --- מרכז המסך (שאלה) ---
    q_num = st.session_state.current_q
    q_data = st.session_state.exam_data.get(q_num)

    if q_data:
        st.subheader(f"שאלה {q_num}")
        st.write(q_data["question"])
