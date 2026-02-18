import streamlit as st
import time
import logic 

# הגדרת דף
st.set_page_config(layout="centered")

# הזרקת סטייל דרך רכיב HTML ייעודי (מבודד) - זה לא גורם ל-TypeError
st.components.v1.html("""
    <style>
        /* פקודה לדפדפן ליישר את הכל לימין */
        html, body, .main {
            direction: rtl !important;
            text-align: right !important;
        }
    </style>
    """, height=0)

def main():
    # משיכת שם משתמש
    try:
        user_name = st.query_params.get("user", "אורח")
    except:
        user_name = "אורח"

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- שימוש ב-Columns ליישור ידני אם ה-CSS נכשל ---
    col_main = st.columns([1])[0]

    with col_main:
        if st.session_state.page_state == 'intro':
            st.header(f"שלום {user_name}")
            st.write("בחינה מקוצרת: 10 שאלות | דקה אחת")
            
            # שימוש ב-Container כדי לשמור על סדר
            with st.container():
                agreed = st.checkbox("אישור הנחיות")
                if agreed:
                    if st.button("התחל"):
                        logic.init_exam()
                        st.session_state.start_time = time.time()
                        st.session_state.page_state = 'exam'
                        st.rerun()

        elif st.session_state.page_state == 'exam':
            logic.run_exam()

        elif st.session_state.page_state == 'results':
            logic.calculate_results()

        st.divider()
        if st.button("🔙 יציאה"):
            st.session_state.page_state = 'intro'
            st.rerun()

if __name__ == "__main__":
    main()
