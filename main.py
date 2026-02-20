# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם
user_name = st.query_params.get("user", "אורח")

# 2. הלינק לחזרה (באותו עמוד)
base_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
back_url = f"{base_url}?user={user_name.replace(' ', '%20')}"

# CSS - צמצום הסטריפ ועיצוב הכפתור
st.markdown(f"""
    <style>
    * {{ direction: rtl; text-align: right; }}
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* סטריפ מצומצם וצפוף */
    .header-box {{
        display: flex;
        align-items: center;
        gap: 25px;
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 20px;
    }}

    .logo-text {{ font-size: 1.3rem; font-weight: bold; }}
    .user-text {{ font-size: 1.1rem; font-weight: 900; }}

    /* כפתור שעובד בתוך אותו דף */
    .home-link {{
        text-decoration: none !important;
        color: #31333f !important;
        border: 1px solid #d1d5db !important;
        padding: 5px 15px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
        background-color: white !important;
        transition: 0.2s;
    }}
    .home-link:hover {{
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }}
    
    .block-container {{ max-width: 800px; margin: auto; }}
    </style>

    <div class="header-box">
        <div class="logo-text">🏠 מתווך בקליק</div>
        <div class="user-text">👤 {user_name}</div>
        <a href="{back_url}" target="_top" class="home-link">לתפריט הראשי</a>
    </div>
""", unsafe_allow_html=True)

# אתחול לוגיקה
initialize_exam()

# 3. דף ההסבר
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
