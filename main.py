# ==========================================
# Project Identification: C-01
# File: main.py
# Version: 1218-G9 (Clean Frame for Integration)
# Anchor: 1213
# ==========================================

import streamlit as st
import time

# הגדרות דף - ללא כותרת (Title) בדפדפן כדי לא להתנגש
st.set_page_config(layout="centered")

# הסתרת רכיבי Streamlit מובנים (תפריט, Footer מקורי, Header) כדי שייראה כחלק מהאפליקציה הראשית
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { direction: RTL; text-align: right; }
    
    /* תפריט תחתון נקי */
    .footer-nav {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        border-top: 1px solid #ddd;
        text-align: center;
        z-index: 100;
    }
    </style>
    """, unsafe_content_html=True)

def main():
    # --- משיכת שם המשתמש מה-URL (ירושה מהאפליקציה הראשית) ---
    query_params = st.query_params
    user_name = query_params.get("user", "אורח")

    # ניהול מצבי דפים
    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # גוף האפליקציה (בלי כותרת גדולה, רק התוכן הרלוונטי)
    
    if st.session_state.page_state == 'intro':
        st.write(f"שלום **{user_name}**, אנא קרא/י את ההנחיות:")
        st.info("בחינה זו כוללת 25 שאלות. זמן מוקצב: 3 דקות. בסיום הזמן המערכת תינעל.")
        
        # צ'ק-בוקס חובה
        if st.checkbox("קראתי ואני מאשר/ת"):
            if st.button("התחל בחינה"):
                st.session_state.page_state = 'exam'
                st.session_state.start_time = time.time()
                st.rerun()

    elif st.session_state.page_state == 'exam':
        # כאן תבוא הפריסה של ה-5 שאלות (logic.py)
        st.write("---") 
        st.write("כאן רצות השאלות...")

    # --- תפריט ניווט תחתון קבוע ---
    st.markdown("---") # רווח ויזואלי מהתוכן
    col_back = st.columns([1, 1, 1])
    with col_back[1]: # כפתור ממורכז למטה
        if st.button("🔙 חזרה לתפריט"):
            st.session_state.page_state = 'intro'
            st.rerun()

if __name__ == "__main__":
    main()
