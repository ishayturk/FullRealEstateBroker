# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam, fetch_next_question

st.set_page_config(
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 1. קליטת שם המשתמש
user_name = st.query_params.get("user", "אורח")

# 2. הכנת הלינק לחזרה
base_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
encoded_name = user_name.replace(' ', '%20')
back_url = f"{base_url}?user={encoded_name}"

# CSS - עיצוב הסטריפ והכפתור בשורה אחת
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .top-strip {{
        position: relative;
        top: 10px; 
        width: 100%;
        height: 50px;
        background-color: white;
        padding: 0 25px;
        direction: rtl;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 25px;
        display: block; /* שינוי לבלוק כדי לאפשר הצפה */
    }}
    
    .strip-right {{ 
        float: right; 
        display: flex; 
        align-items: center; 
        gap: 20px; 
        height: 50px;
    }}
    
    .strip-left {{ 
        float: left; 
        display: flex; 
        align-items: center; 
        height: 50px;
    }}
    
    .strip-logo {{ font-weight: bold; font-size: 1.2rem; color: #31333f; }}
    .strip-user {{ font-weight: 900 !important; font-size: 1.1rem; }}

    .back-link-btn {{
        text-decoration: none !important;
        color: #31333f !important;
        border: 1px solid #d1d5db !important;
        padding: 4px 15px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 0.85rem !important;
        transition: 0.2s;
        display: inline-block;
        line-height: 1.5;
    }}
    
    .back-link-btn:hover {{
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
        background-color: #fffafa !important;
    }}

    .block-container {{ 
        direction: rtl; 
        max-width: 800px; 
        margin: auto; 
        padding-top: 0px !important; 
    }}
    </style>

    <div class="top-strip">
        <div class="strip-right">
            <div class="strip-logo">🏠 מתווך בקליק</div>
            <div class="strip-user">👤 <b>{user_name}</b></div>
        </div>
        <div class="strip-left">
            <a href="{back_url}" target="_self" class="back-link-btn">
                חזרה לתפריט הראשי
            </a>
        </div>
        <div style="clear: both;"></div>
    </div>
    <hr style="margin-top: 5px; border: 0; border-top: 1px solid #f0f0f0; 
    margin-bottom: 30px;">
""", unsafe_allow_html=True)

# לוגיקת בחינה (ללא שינוי)
initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.markdown('<div style="text-align: right; direction: rtl;">', 
                unsafe_allow_html=True)
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
    st.write("6. ציון עובר: 60.")
    st.write("7. חל איסור על שימוש בחומר עזר.")
    st.divider()
    
    msg = "קראתי את ההוראות ואני מוכן להתחיל"
    agree = st.checkbox(msg)
    if st.button("התחל בחינה", disabled=not agree):
        st.session_state.step = "exam_run"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
