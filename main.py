# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
import streamlit.components.v1 as components
from logic import initialize_exam

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם
user_name = st.query_params.get("user", "אורח")

# 2. כתובת החזרה
base_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
back_url = f"{base_url}?user={user_name.replace(' ', '%20')}"

# CSS לצמצום תוכן העמוד
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { max-width: 800px; margin: auto; padding-top: 5px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. סטריפ צפוף עם JavaScript לניווט באותו דף
header_html = f"""
    <div style="display: flex; align-items: center; justify-content: flex-start; 
                gap: 25px; direction: rtl; font-family: sans-serif; 
                border-bottom: 1px solid #f0f0f0; padding-bottom: 10px;">
        <div style="font-size: 1.2rem; font-weight: bold; white-space: nowrap;">🏠 מתווך בקליק</div>
        <div style="font-size: 1.1rem; font-weight: 900; white-space: nowrap;">👤 {user_name}</div>
        <button onclick="window.parent.location.href='{back_url}'" 
                style="cursor: pointer; background: white; border: 1px solid #d1d5db; 
                       padding: 5px 15px; border-radius: 8px; font-weight: bold; 
                       font-size: 0.85rem; color: #31333f;">
            לתפריט הראשי
        </button>
    </div>
"""

components.html(header_html, height=60)

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
