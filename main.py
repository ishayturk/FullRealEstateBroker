import streamlit as st
import time
import logic  # ייבוא המנוע שבנינו

# הגדרות דף - חייב להיות השורה הראשונה
st.set_page_config(layout="centered")

# הזרקת CSS בצורה בטוחה יותר כדי למנוע TypeError
footer_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { direction: RTL; text-align: right; }
    .footer-nav {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        border-top: 1px solid #ddd;
        text-align: center;
        z-index: 100;
    }
</style>
"""
st.markdown(footer_style, unsafe_content_html=True)

def main():
    # משיכת שם משתמש מה-URL
    user_name = st.query_params.get("user", "אורח")

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- ניווט דפים ---
    
    if st.session_state.page_state == 'intro':
        st.write(f"שלום **{user_name}**, ברוך הבא למערכת הבחינות.")
        st.info("בחינה: 1213 | זמן: 3 דקות | 25 שאלות")
        
        if st.checkbox("אני מאשר/ת את תנאי הבחינה"):
            if st.button("התחל בחינה"):
                logic.init_exam() # אתחול הנתונים מ-logic.py
                st.session_state.start_time = time.time()
                st.session_state.page_state = 'exam'
                st.rerun()

    elif st.session_state.page_state == 'exam':
        logic.run_exam() # הרצת המנוע של ה-8 שלבים

    elif st.session_state.page_state == 'results':
        logic.calculate_results() # דף המשוב

    # --- תפריט תחתון קבוע ---
    st.markdown("---")
    if st.button("🔙 יציאה/חזרה"):
        st.session_state.page_state = 'intro'
        # כאן אפשר להוסיף ניקוי של ה-session_state אם רוצים בחינה חדשה לגמרי
        st.rerun()

if __name__ == "__main__":
    main()
