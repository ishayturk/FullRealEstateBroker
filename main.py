import streamlit as st
import time
import logic 

# הגדרה ראשונה
st.set_page_config(layout="centered")

# שימוש ברכיב HTML ייעודי במקום markdown למניעת TypeError
st.components.v1.html("""
    <style>
        body { direction: RTL; text-align: right; }
        .stApp { direction: RTL; text-align: right; }
    </style>
    """, height=0)

def main():
    # ניסיון משיכה בטוח של query_params
    try:
        user_name = st.query_params.get("user", "אורח")
    except:
        user_name = "אורח"

    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'intro'

    if st.session_state.page_state == 'intro':
        st.write(f"שלום **{user_name}**")
        st.info("בחינה: 1213 | 3 דקות | 25 שאלות")
        
        if st.checkbox("אני מאשר/ת את התנאים"):
            if st.button("התחל בחינה"):
                logic.init_exam()
                st.session_state.start_time = time.time()
                st.session_state.page_state = 'exam'
                st.rerun()

    elif st.session_state.page_state == 'exam':
        logic.run_exam()

    elif st.session_state.page_state == 'results':
        logic.calculate_results()

    # תפריט תחתון פשוט ללא CSS מורכב
    st.divider()
    if st.button("🔙 חזרה/יציאה"):
        st.session_state.page_state = 'intro'
        st.rerun()

if __name__ == "__main__":
    main()
