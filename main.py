# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam, fetch_next_question

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם המשתמש
user_name = st.query_params.get("user", "אורח")

# 2. הלינק המדויק לאפליקציית הלימוד
study_app_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
back_url = f"{study_app_url}?user={user_name.replace(' ', '%20')}"

# CSS לעיצוב הסטריפ והוראות המבחן
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
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 25px;
        direction: rtl;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 15px;
    }}
    
    .strip-right {{ display: flex; align-items: center; gap: 20px; }}
    .strip-logo {{ font-weight: bold; font-size: 1.2rem; color: #31333f; }}
    .strip-user {{ font-weight: 900 !important; font-size: 1.1rem; color: #31333f; }}

    .block-container {{ direction: rtl; max-width: 800px; margin: auto; padding-top: 0px !important; }}
    h1 {{ font-size: 2rem !important; margin-top: 0px !important; margin-bottom: 15px !important; text-align: center !important; width: 100%; }}
    .instructions-box {{ text-align: right; direction: rtl; line-height: 1.4; }}
    </style>
""", unsafe_allow_html=True)

# 3. הזרקת הסטריפ עם רכיב HTML ייעודי לכפתור כדי להבטיח פעולה
st.markdown(f"""
    <div class="top-strip">
        <div class="strip-right">
            <div class="strip-logo">🏠 מתווך בקליק</div>
            <div class="strip-user">👤 <b>{user_name}</b></div>
        </div>
        <div class="strip-back">
            <button onclick="window.parent.location.href='{back_url}'" 
                style="cursor: pointer; background: transparent; border: 1px solid #d1d5db; 
                padding: 6px 18px; border-radius: 8px; font-weight: bold; font-size: 0.9rem; color: #31333f;">
                חזרה לתפריט הראשי
            </button>
        </div>
    </div>
""", unsafe_allow_html=True)

# אתחול לוגיקה
initialize_exam()

# מסך ההסבר
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.markdown('<div class="instructions-box">', unsafe_allow_html=True)
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
