# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם המשתמש
user_name = st.query_params.get("user", "אורח")

# 2. הלינק לאפליקציית הלימוד
study_app_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
encoded_name = user_name.replace(' ', '%20')
back_url = f"{study_app_url}?user={encoded_name}"

# CSS בסיסי ליישור
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. הסטריפ העליון במבנה שעבד
c_right, c_mid, c_left = st.columns([3, 1.5, 1.5])

with c_right:
    st.markdown(f"### 🏠 מתווך בקליק")

with c_mid:
    st.markdown(f"👤 **{user_name}**")

with c_left:
    st.link_button("לתפריט הראשי", back_url)

st.divider()

# אתחול לוגיקה
initialize_exam()

# 4. דף ההסבר המקורי
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
