import streamlit as st
import time
import logic 

# הגדרה ראשונית
st.set_page_config(layout="centered")

# הזרקת סטייל ייעודי שפועל על המעטפת של Streamlit
st.markdown("""
    <style>
    /* יישור כללי לימין */
    .stApp {
        direction: RTL;
        text-align: right;
    }
    /* יישור ספציפי לכפתורים ותפריטים */
    div.stButton > button {
        direction: rtl;
    }
    /* תיקון יישור לטקסטים ושאלות */
    .stMarkdown, .stText, .stHeader, p, label {
        text-align: right !important;
        direction: rtl !important;
    }
    /* יישור רדיו (תשובות) */
    [data-testid="stWidgetLabel"] {
        text-align: right !important;
        direction: rtl !important;
    }
    </style>
    """, unsafe_content_html=True)

def main():
    # משיכת שם משתמש
    user_name = st.query_params.get("user", "אורח")

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- דף פתיחה ---
    if st.session_state.page_state == 'intro':
        st.header(f"שלום {user_name}")
        st.subheader("הנחיות לבחינה המקוצרת")
        st.write("• 10 שאלות")
        st.write("• דקה אחת (60 שניות)")
        
        if st.checkbox("אני מאשר/ת את ההנחיות"):
            if st.button("התחל בחינה"):
                logic.init_exam()
                st.session_state.start_time = time.time()
                st.session_state.page_state = 'exam'
                st.rerun()

    # --- דף בחינה ---
    elif st.session_state.page_state == 'exam':
        logic.run_exam()

    # --- דף תוצאות ---
    elif st.session_state.page_state == 'results':
        logic.calculate_results()

    # תפריט תחתון
    st.divider()
    if st.button("🔙 יציאה"):
        # איפוס נתונים ביציאה
        if 'exam_data' in st.session_state: del st.session_state.exam_data
        st.session_state.page_state = 'intro'
        st.rerun()

if __name__ == "__main__":
    main()
