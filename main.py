# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam, fetch_next_question

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# קליטת שם המשתמש מהכתובת
user_name = st.query_params.get("user", "אורח")

# CSS מעודכן לצמצום רווחים והעלאת התוכן למעלה
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .top-strip {{
        position: relative;
        top: 10px; /* צמוד יותר למעלה */
        width: 100%;
        height: 50px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 25px;
        direction: rtl;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 15px; /* צמצום משמעותי של הרווח מתחת לסטריפ */
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
        display: flex;
        align-items: center;
        gap: 8px;
        color: #31333f;
    }}
    
    .back-btn-placeholder {{
        border: 1px solid #d1d5db;
        padding: 6px 18px;
        border-radius: 8px;
        font-weight: bold;
        color: #9ca3af;
        background-color: transparent;
        cursor: not-allowed;
    }}

    .block-container {{
        direction: rtl;
        max-width: 800px;
        margin: auto;
        padding-top: 0px !important;
    }}
    
    .instructions-box {{
        text-align: right;
        direction: rtl;
        line-height: 1.4; /* צמצום מרווח בין שורות */
    }}
    
    /* העלאת הכותרת וצמצום רווחים */
    h1 {{ 
        font-size: 2rem !important; 
        margin-top: 0px !important; 
        margin-bottom: 10px !important; 
        padding-top: 0px !important;
    }}
    
    .stDivider {{
        margin-top: 5px !important;
        margin-bottom: 5px !important;
    }}

    /* צמצום הרווח סביב ה-Checkbox */
    div[data-testid="stCheckbox"] {{
        margin-top: -10px !important;
    }}
    </style>

    <div class="top-strip">
        <div class="strip-right">
            <div class="strip-logo">🏠 מתווך בקליק</div>
            <div class="strip-user">👤 <b>{user_name}</b></div>
        </div>
        <div class="strip-back">
            <span class="back-btn-placeholder">חזרה לתפריט הראשי</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# אתחול לוגיקה
initialize_exam()

# מסך ההסבר
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<div class="instructions-box">', unsafe_allow_html=True)
    st.title("הוראות למבחן רישויי מקרקעין")

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
