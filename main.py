import streamlit as st
import pandas as pd
import time
import os
import random
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

# הגדרות עמוד ויישור לימין (RTL)
st.set_page_config(page_title="פורטל הכנה למתווכים", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    .main-nav { display: flex; gap: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# אתחול מצב אפליקציה (Login -> Menu -> Exam/Study)
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'login'

# --- 1. דף כניסה (Login Page) ---
if st.session_state.app_mode == 'login':
    st.title("🔑 כניסה למערכת")
    user_name = st.text_input("שם משתמש")
    if st.button("התחבר"):
        if user_name:
            st.session_state.user = user_name
            st.session_state.app_mode = 'main_menu'
            st.rerun()

# --- 2. תפריט ראשי (Main Menu) ---
elif st.session_state.app_mode == 'main_menu':
    st.title(f"שלום, {st.session_state.get('user', 'אורח')}")
    st.subheader("מה ברצונך לעשות היום?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 מרכז לימודים ושיעורים"):
            st.session_state.app_mode = 'study'
            st.rerun()
    with col2:
        if st.button("📝 תרגול בחינה (25 שאלות)"):
            st.session_state.step = 'instructions'
            st.session_state.app_mode = 'exam_mode'
            st.rerun()

# --- 3. מרכז לימודים (Study Center) ---
elif st.session_state.app_mode == 'study':
    st.title("📚 מרכז לימודים")
    if st.button("🔙 חזרה לתפריט"):
        st.session_state.app_mode = 'main_menu'
        st.rerun()
    
    st.write("כאן יופיעו חומרי הלימוד והשיעורים שלך.")
    # כאן ניתן להוסיף רשימת שיעורים, PDF או וידאו

# --- 4. מצב בחינה (Exam Mode) ---
elif st.session_state.app_mode == 'exam_mode':
    # כאן נכנסת הלוגיקה של הבחינה (C-05.2)
    # לצורך קיצור, אני מניח שקובץ ה-CSV נטען וקיים כפי שהוגדר קודם
    
    if st.session_state.get('step') == 'instructions':
        # קריאה ל-show_instructions() מ-ui_utils
        st.title("📋 הוראות לבחינה")
        st.write("הבחינה כוללת 25 שאלות, זמן מוקצב: 3 דקות.")
        if st.button("התחל כעת"):
            st.session_state.start_time = time.time()
            st.session_state.step = 'exam_active'
            st.rerun()
        if st.button("ביטול וחזרה לתפריט"):
            st.session_state.app_mode = 'main_menu'
            st.rerun()

    elif st.session_state.get('step') == 'exam_active':
        # כאן מורץ המנוע של ה-25 שאלות
        st.write("המבחן רץ...")
        # (המשך הקוד של C-05.2 מיושם כאן)
