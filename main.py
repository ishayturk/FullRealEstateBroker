# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# ה-CSS המדויק מהאפליקציה השנייה
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    
    .header-container {
        display: flex;
        align-items: center;
        gap: 45px;
        margin-bottom: 30px;
    }
    
    .header-title { 
        font-size: 2.5rem !important; 
        font-weight: bold !important; 
        margin: 0 !important;
        white-space: nowrap;
    }
    
    .header-user { 
        font-size: 1.2rem !important; 
        font-weight: 900 !important;
        color: #31333f; 
        white-space: nowrap;
        margin-top: 10px;
    }

    /* כפתור הלינק המדויק שעבד */
    .stLinkButton>a { 
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        width: 100% !important; 
        border-radius: 8px !important; 
        font-weight: bold !important; 
        height: 3em !important; 
        background-color: transparent !important;
        color: #31333f !important;
        border: 1px solid #d1d5db !important;
        text-decoration: none !important;
        transition: 0.2s;
    }
    .stLinkButton>a:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. קליטת שם
user_name = st.query_params.get("user", "אורח")

# 2. כותרת וסטריפ (במבנה של האפליקציה שעבדה)
c1, c2, c3 = st.columns([1.5, 1.5, 3])

with c1:
    # שימוש ב-st.link_button המקורי
    u_name = user_name.replace(" ", "%20")
    t_url = f"https://ishayturk-realtor-app-app-kk1gme.streamlit.app/?user={u_name}"
    st.link_button("לתפריט הראשי", t_url)

with c2:
    st.markdown(f'<div class="header-user">👤 <b>{user_name}</b></div>', 
                unsafe_allow_html=True)

with c3:
    st.markdown('<div class="header-title">🏠 מתווך בקליק</div>', 
                unsafe_allow_html=True)

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
