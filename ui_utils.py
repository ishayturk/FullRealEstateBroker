# ui_utils.py | Version: C-01
import streamlit as st

def apply_design():
    """
    מזריק עיצוב CSS בסיסי ותומך RTL.
    """
    st.markdown("""
    <style>
        * { direction: rtl; text-align: right; }
        .stButton>button { 
            width: 100%; 
            border-radius: 8px; 
            font-weight: bold; 
            height: 3.5em; 
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
        }
        .stButton>button:hover {
            border-color: #007bff;
            color: #007bff;
        }
    </style>
    """, unsafe_allow_html=True)

def navigation_footer():
    """
    מציג כפתור חזרה קבוע בתחתית הדף.
    """
    st.write("---")
    if st.button("🏠 חזרה לתפריט ראשי"):
        st.session_state.step = "menu"
        st.rerun()
