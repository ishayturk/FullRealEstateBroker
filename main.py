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

# CSS - שבירת שורות לשמירה על Git
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .top-strip {{
        position: relative;
        top: 10px; 
        width: 100%;
        height: 60px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 25px;
        direction: rtl;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 25px;
    }}
    
    .strip-right {{ 
        display: flex; 
        align-items: center; 
        gap: 20px; 
    }}
    
    .strip-logo {{ 
        font-weight: bold; 
        font-size: 1.2rem; 
        color: #31333f; 
    }}
    
    .strip-user {{ 
        font-weight: 900 !important; 
        font-size: 1.1rem; 
        color: #31333f; 
    }}

    .stLinkButton > a {{
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        border-radius: 8px !important; 
        font-weight: bold !important; 
        background-color: transparent !important;
        color: #31333f !important;
        border: 1px solid #d1d5db !important;
        text-decoration: none !important;
        transition: 0.2s;
        padding: 4px 15px !important;
        font-size: 0.85rem !important;
        height: 35px !important;
    }}
    
    .stLinkButton > a:hover {{
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }}

    .block-container {{ 
        direction: rtl; 
        max-width: 800px; 
        margin: auto; 
        padding-top: 0px !important; 
    }}
    
    h1 {{ 
        font-size: 2rem !important; 
        margin: 0 0 15px 0 !important; 
        text-align: center !important; 
        width: 100%; 
    }}
    
    .instructions-box {{ 
        text-align: right; 
        direction: rtl; 
        line-height: 1.4; 
    }}
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון
c_right, c_left = st.columns([3, 1])

with c_right:
    st.markdown(f"""
        <div class="top-strip" style="border: none; margin: 0; padding: 0;">
            <div class="strip-right">
                <div class="strip-logo">🏠 מתווך בקליק</div>
                <div class="strip-user">👤 <b>{user_name}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c_left:
    st.write("") 
    st.link_button("חזרה לתפריט הראשי", back_url)

st.markdown("""
    <hr style="margin-top: -10px; border: 0; 
    border-top: 1px solid #f0f0f0; margin-bottom: 30px;">
    """, unsafe_allow_html=True)

# לוגיקת בחינה
initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.markdown('<div class="instructions-box">', unsafe_allow_html=True)
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
