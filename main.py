import streamlit as st
import time
import logic 

# הגדרת דף
st.set_page_config(layout="centered")

# הזרקת סטייל בשורות בודדות כדי למנוע את ה-TypeError של Python 3.13
st.markdown('<style>div.stApp { direction: rtl; text-align: right; }</style>', unsafe_content_html=True)
st.markdown('<style>div.stMarkdown { text-align: right; }</style>', unsafe_content_html=True)
st.markdown('<style>div.row-widget { text-align: right; }</style>', unsafe_content_html=True)
st.markdown('<style>.stRadio > label { text-align: right; direction: rtl; }</style>', unsafe_content_html=True)

def main():
    # משיכת שם משתמש
    user_name = st.query_params.get("user", "אורח")

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- ניווט דפים ---
    if st.session_state.page_state == 'intro':
        st.header(f"שלום {user_name}")
        st.write("בחינה מקוצרת: 10 שאלות | דקה אחת")
        
        if st.checkbox("אישור הנחיות"):
            if st.button("התחל"):
                logic.init_exam()
                st.session_state.start_time = time.time()
                st.session_state.page_state = 'exam'
                st.rerun()

    elif st.session_state.page_state == 'exam':
        logic.run_exam()

    elif st.session_state.page_state == 'results':
        logic.calculate_results()

    # תפריט תחתון
    st.divider()
    if st.button("🔙 יציאה"):
        st.session_state.page_state = 'intro'
        st.rerun()

if __name__ == "__main__":
    main()
