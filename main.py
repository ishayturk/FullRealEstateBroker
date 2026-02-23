# File: main.py
# Version: V222
# Date: 2026-02-23
# Time: 18:30

import streamlit as st
from logic import run_exam_logic

# הגדרות עמוד כלליות
st.set_page_config(page_title="מערכת רשם המתווכים", layout="wide")

# CSS מופרד ל-3 חלקים: General, Desktop, Mobile
st.markdown("""
    <style>
    /* General Section */
    .main { direction: rtl; text-align: right; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; }
    
    /* Desktop Section */
    @media (min-width: 1024px) {
        .stSidebar { width: 250px !important; }
        .main-content { padding: 2rem; }
    }
    
    /* Mobile Section */
    @media (max-width: 1023px) {
        .stSidebar { width: 100% !important; }
        .main-content { padding: 0.5rem; }
        h1 { font-size: 1.5rem; }
    }
    </style>
""", unsafe_allow_html=True)

# הרצת הלוגיקה המרכזית
if __name__ == "__main__":
    run_exam_logic()

# סוף קובץ
