# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם
user_name = st.query_params.get("user", "אורח")

# 2. קישור חזרה
base_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
back_url = f"{base_url}?user={user_name.replace(' ', '%20')}"

# CSS בסיסי להסתרת אלמנטים מיותרים
st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 10px !important;}
    
    /* עיצוב שם המשתמש והלוגו */
    .strip-text {
        font-size: 1.1rem;
        font-weight: 900;
        display: flex;
        align-items: center;
        gap: 15px;
        height: 40px;
    }

    /* עיצוב הלחצן שייראה עדין */
    .stLinkButton > a {
        border: 1px solid #d1d5db !important;
        background: transparent !important;
        color: #31333f !important;
        font-weight: bold !important;
        height: 35px !important;
        line-height: 35px !important;
        padding: 0 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. הסטריפ העליון באמצעות עמודות - מובטח שיעבוד
c1, c2, c3 = st.columns([2, 2, 1])

with c1:
    st.markdown(f"""
        <div class="strip-text">
            🏠 מתווך בקליק | 👤 {user_name}
        </div>
    """, unsafe_allow_html=True)

with c3:
    # כפתור רשמי, טקסט קצר, שורה אחת
    st.link_button("תפריט ראשי", back_url)

st.divider()

# לוגיקת בחינה
initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן")
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.divider()
    
    if st.checkbox("אני מוכן להתחיל"):
        if st.button("התחל בחינה"):
            st.session_state.step = "exam_run"
            st.rerun()
