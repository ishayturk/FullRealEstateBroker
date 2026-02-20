# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam, fetch_next_question

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם המשתמש
user_name = st.query_params.get("user", "אורח")

# 2. הכנת הלינק לחזרה
study_app_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
encoded_name = user_name.replace(' ', '%20')
back_url = f"{study_app_url}?user={encoded_name}"

# CSS שמעצב גם את הסטריפ וגם את הכפתור של Streamlit שיונח בתוכו
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* עיצוב הסטריפ */
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
        margin-bottom: 15px;
    }}
    
    .strip-right {{
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    
    .strip-logo {{ font-weight: bold; font-size: 1.2rem; color: #31333f; }}
    .strip-user {{ font-weight: 900 !important; font-size: 1.1rem; color: #31333f; }}

    /* הפיכת הכפתור הסטנדרטי של Streamlit למעוצב עבור הסטריפ */
    div[data-testid="stLinkButton"] {{
        margin: 0 !important;
    }}
    div[data-testid="stLinkButton"] > a {{
        background-color: transparent !important;
        border: 1px solid #d1d5db !important;
        color: #31333f !important;
        padding: 6px 18px !important;
        font-weight: bold !important;
        text-decoration: none !important;
        border-radius: 8px !important;
        height: auto !important;
        line-height: 1.5 !important;
    }}
    div[data-testid="stLinkButton"] > a:hover {{
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }}

    .block-container {{ direction: rtl; max-width: 800px; margin: auto; padding-top: 0px !important; }}
    h1 {{ font-size: 2rem !important; margin: 0 0 15px 0 !important; text-align: center !important; }}
    .instructions-box {{ text-align: right; direction: rtl; line-height: 1.4; }}
    </style>
""", unsafe_allow_html=True)

# יצירת הסטריפ עם עמודות כדי לשלב את כפתור ה-Streamlit בצורה מושלמת
col_right, col_left = st.columns([3, 1])

with col_right:
    # הזרקת ה-HTML רק עבור הצד הימני (לוגו ושם)
    st.markdown(f"""
        <div class="top-strip" style="border-bottom: none; margin-bottom: 0;">
            <div class="strip-right">
                <div class="strip-logo">🏠 מתווך בקליק</div>
                <div class="strip-user">👤 <b>{user_name}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_left:
    # שימוש בכפתור לינק רשמי של Streamlit - זה חייב לעבוד
    st.write("") # ריווח קטן
    st.link_button("חזרה לתפריט הראשי", back_url)

# קו מפריד דק מתחת לכל הסטריפ
st.markdown('<hr style="margin-top: -10px; border: 0; border-top: 1px solid #f0f0f0;">', unsafe_allow_html=True)

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
