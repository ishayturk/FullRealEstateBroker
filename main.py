# ==========================================
# Project Identification: C-01
# File: main.py
# Version: 1218-G11 (Zero-CSS Version)
# Anchor: 1213
# ==========================================

import streamlit as st
import time
import logic 

# הגדרה רגילה לחלוטין - בלי CSS, בלי Markdown בעייתי
st.set_page_config(layout="wide")

def main():
    # משיכת שם משתמש בצורה בטוחה
    user_name = st.query_params.get("user", "אורח")

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- שימוש בעמודות כדי לדחוף טקסט לימין באופן טבעי ---
    col_empty, col_content = st.columns([1, 4]) 

    with col_content:
        if st.session_state.page_state == 'intro':
            st.header(f"שלום {user_name}")
            st.write("בחינה: 10 שאלות | דקה אחת")
            
            if st.checkbox("אני מאשר/ת את התנאים"):
                if st.button("התחל בחינה"):
                    logic.init_exam()
                    st.session_state.start_time = time.time()
                    st.session_state.page_state = 'exam'
                    st.rerun()

        elif st.session_state.page_state == 'exam':
            logic.run_exam()

        elif st.session_state.page_state == 'results':
            logic.calculate_results()

    # Sidebar פשוט ללא עיצוב
    with st.sidebar:
        st.title("Ludo Exam")
        if st.button("יציאה"):
            st.session_state.page_state = 'intro'
            st.rerun()

if __name__ == "__main__":
    main()
