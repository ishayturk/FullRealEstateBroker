# ==========================================
# Project Identification: C-01
# File: main.py
# Version: 1218-G10 (Stable RTL & Sidebar)
# Anchor: 1213
# ==========================================

import streamlit as st
import time
import logic  # מוודא שקובץ logic.py המעודכן נמצא באותה תיקייה

# הגדרת פריסה רחבה כדי שה-Sidebar ייראה טוב במחשב
st.set_page_config(layout="wide", page_title="Ludo Exam System")

# הזרקת RTL בשורה אחת למניעת TypeError ב-Python 3.13
st.markdown('<style>html,body,[data-testid="stAppViewContainer"]{direction:rtl;text-align:right!important;}[data-testid="stSidebar"]{direction:rtl;text-align:right!important;}.stMarkdown,p,label,h1,h2,h3,h4{text-align:right!important;direction:rtl!important;}</style>', unsafe_content_html=True)

def main():
    # משיכת שם משתמש מה-URL (ירושה מהאפליקציה הראשית)
    user_name = st.query_params.get("user", "אורח")

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- ניהול מצבי דפים ---
    
    if st.session_state.page_state == 'intro':
        st.header(f"שלום {user_name}")
        st.subheader("ברוכים הבאים לבחינה (C-01)")
        st.write("בחינה זו כוללת 10 שאלות. זמן מוקצב: דקה אחת.")
        
        st.divider()
        if st.checkbox("קראתי ואני מאשר/ת את תנאי הבחינה"):
            if st.button("התחל בחינה עכשיו", type="primary"):
                logic.init_exam()
                st.session_state.start_time = time.time()
                st.session_state.page_state = 'exam'
                st.rerun()

    elif st.session_state.page_state == 'exam':
        # קריאה למנוע הבחינה מ-logic.py (כולל ה-Sidebar)
        logic.run_exam()

    elif st.session_state.page_state == 'results':
        # דף סיכום ותוצאות
        logic.calculate_results()
        if st.button("חזרה לדף הבית"):
            st.session_state.page_state = 'intro'
            st.rerun()

    # כפתור יציאה קבוע בתחתית ה-Sidebar (יופיע בכל השלבים)
    with st.sidebar:
        st.divider()
        if st.button("🔙 יציאה/סגירה"):
            st.session_state.page_state = 'intro'
            st.rerun()

if __name__ == "__main__":
    main()
