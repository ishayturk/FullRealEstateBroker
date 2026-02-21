# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: exam_v03_balanced | Date: 21/02/2026 | 23:25
import streamlit as st
from logic import initialize_exam

st.set_page_config(page_title="מתווך בקליק - בחינה", layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם משתמש מה-URL
user_name = st.query_params.get("user", "אורח")

# 2. עיצוב CSS - צמצום רווחים ושימור גדלים
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* מרכוז התוכן */
    .block-container { 
        max-width: 800px !important; 
        margin: auto !important; 
        padding-top: 0.5rem !important;
    }
    
    /* הסטריפ העליון - מראה מקורי ללא קו */
    .fixed-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
        margin-bottom: 0px;
    }

    /* הצמדת הכותרת הראשית למעלה */
    h1 {
        margin-top: -15px !important;
        padding-top: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. הכותרת (בגודל המקורי)
st.markdown(f"""
    <div class="fixed-header">
        <div>
            <span style="font-size: 1.2rem; font-weight: bold;">🏠 מתווך בקליק - מערכת בחינות</span>
        </div>
        <div>
            👤 <b>{user_name}</b>
        </div>
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
    
    # רווח לפני הצ'קבוקס כדי שלא יהיה צמוד מידי לטקסט
    st.write("")
    agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    
    # רווח בודד בין הצ'קבוקס לכפתור
    st.write("")
    if st.button("התחל בחינה", disabled=not agree):
        st.session_state.step = "exam_run"
        st.rerun()

# עמוד המבחן
elif st.session_state.step == "exam_run":
    st.write("כאן תוצג מערכת השאלות...")

# סוף קובץ
