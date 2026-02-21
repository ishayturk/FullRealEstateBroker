# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: exam_v01 | Date: 21/02/2026 | 22:45
import streamlit as st
from logic import initialize_exam

st.set_page_config(page_title="מתווך בקליק - בחינה", layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם משתמש מה-URL
user_name = st.query_params.get("user", "אורח")

# 2. עיצוב CSS - מרכוז תוכן וכותרת קבועה ללא לינקים
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* מרכוז התוכן של האפליקציה למניעת מריחה */
    .block-container { 
        max-width: 900px !important; 
        margin: auto !important; 
        padding-top: 1rem !important;
    }
    
    /* עיצוב הכותרת הקבועה - לוגו ושם משתמש בלבד */
    .fixed-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 25px;
        background-color: #f8f9fa;
        border-bottom: 2px solid #eee;
        margin-bottom: 40px;
        border-radius: 8px;
    }
    .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .app-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #31333F;
    }
    .user-info {
        font-size: 1.1rem;
        font-weight: 600;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# 3. הכותרת המשותפת (מופיעה תמיד בראש כל עמוד במערכת הבחינות)
st.markdown(f"""
    <div class="fixed-header">
        <div class="logo-section">
            <span style="font-size: 1.8rem;">🏠</span>
            <span class="app-title">מתווך בקליק - מערכת בחינות</span>
        </div>
        <div class="user-info">
            👤 <b>{user_name}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# אתחול לוגיקה (session_state)
initialize_exam()

# 4. ניתוב עמודים
if "step" not in st.session_state:
    st.session_state.step = "instructions"

# דף הוראות
if st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    
    st.info("""
    המבחן מדמה את התנאים הרשמיים של רשם המתווכים. 
    השאלות נוצרות בזמן אמת ומבוססות על מאגר בחינות האמת ודיני האתיקה המעודכנים.
    """)
    
    st.markdown("""
    * **מספר שאלות:** 25
    * **זמן מוקצב:** 90 דקות
    * **ניווט:** ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה.
    * **תיקון:** ניתן לחזור אחורה לשאלות שכבר נענו.
    * **ציון עובר:** 60
    """)
    
    st.divider()
    
    agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל בבחינה")
    
    if st.button("התחל בחינה", disabled=not agree):
        st.session_state.step = "exam_run"
        st.rerun()

# עמוד הרצת הבחינה (יושלם בצעד הבא)
elif st.session_state.step == "exam_run":
    st.subheader("הבחינה החלה")
    st.write("כאן תוצג מערכת השאלות והתשובות בזמן אמת.")

# סוף קובץ
