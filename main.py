# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם
user_name = st.query_params.get("user", "אורח")

# 2. הלינק לחזרה
base_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
back_url = f"{base_url}?user={user_name.replace(' ', '%20')}"

# CSS בסיסי ביותר רק ליישור
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { max-width: 800px; margin: auto; }
    </style>
""", unsafe_allow_html=True)

# 3. סטריפ עם קישור HTML נקי (בלי CSS לכפתור - כדי שיעבוד)
st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 20px; padding: 10px; border-bottom: 1px solid #eee;">
        <span style="font-size: 1.2rem; font-weight: bold;">🏠 מתווך בקליק</span>
        <span style="font-size: 1.1rem;">👤 <b>{user_name}</b></span>
        <a href="{back_url}" target="_self" style="color: #0000EE; text-decoration: underline; font-weight: bold;">
            לתפריט הראשי
        </a>
    </div>
""", unsafe_allow_html=True)

# אתחול לוגיקה
initialize_exam()

# 4. דף ההסבר
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
    st.write("6. ציון עובר: 60.")
    st.write("7. חל איסור על שימוש בחומר עזר.")
    st.divider()
    
    agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    if st.button("התחל בחינה", disabled=not agree):
        st.session_state.step = "exam_run"
        st.rerun()
