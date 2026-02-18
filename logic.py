import streamlit as st
import time
import logic 

# הגדרת דף
st.set_page_config(layout="wide", page_title="Ludo Exam")

# הזרקת CSS בשיטה של "שורה אחת" - ככה זה לא יכול לייצר TypeError של רווחים
rtl_css = '<style>div[data-testid="stAppViewContainer"]{direction:rtl;text-align:right;}div[data-testid="stHeader"]{direction:rtl;}div[data-testid="stSidebar"]{direction:rtl;text-align:right;}div[data-testid="stVerticalBlock"]{direction:rtl;text-align:right;}.stMarkdown,p,label,h1,h2,h3,h4{text-align:right!important;direction:rtl!important;}</style>'
st.markdown(rtl_css, unsafe_content_html=True)

def main():
    # משיכת שם משתמש
    user_name = st.query_params.get("user", "אורח")

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    # --- מבנה הדף ---
    if st.session_state.page_state == 'intro':
        st.header(f"שלום {user_name}")
        st.markdown("### בחינה מקוצרת (1213)")
        st.write("• 10 שאלות")
        st.write("• דקה אחת לביצוע")
        
        # מרכוז הכפתור בעזרת עמודות
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.checkbox("אני מאשר/ת את תנאי הבחינה"):
                if st.button("התחל בחינה עכשיו", use_container_width=True):
                    logic.init_exam()
                    st.session_state.start_time = time.time()
                    st.session_state.page_state = 'exam'
                    st.rerun()

    elif st.session_state.page_state == 'exam':
        logic.run_exam()

    elif st.session_state.page_state == 'results':
        logic.calculate_results()

    # תפריט תחתון
    st.sidebar.divider()
    if st.sidebar.button("🔙 יציאה מהבחינה", use_container_width=True):
        st.session_state.page_state = 'intro'
        st.rerun()

if __name__ == "__main__":
    main()
