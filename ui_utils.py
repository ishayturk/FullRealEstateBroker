# ui_utils.py | Version: C-02
import streamlit as st

def apply_design():
    # כותרת ולוגו קבועים שמופיעים בכל דף
    st.markdown("<h1 style='text-align: center;'>🏠 מתווך בקליק</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        * { direction: rtl; text-align: right; }
        .stButton>button { 
            width: 100%; 
            border-radius: 8px; 
            font-weight: bold; 
            height: 3.5em; 
        }
    </style>
    """, unsafe_allow_html=True)

def navigation_footer():
    st.write("---")
    if st.button("🏠 חזרה לתפריט ראשי"):
        # ניקוי זיכרון זמני של שיעור
        st.session_state.lesson_txt = ""
        st.session_state.step = "menu"
        st.rerun()
