# Project: מתווך בקליק | Version: B04
# File: styles.py
import streamlit as st

def apply_styles(version_label):
    """מחיל עיצוב RTL וסידור כפתורים נקי"""
    st.markdown(f"""
    <style>
    /* הגדרת כיוון כללית */
    .stApp {{
        direction: rtl;
        text-align: right;
    }}
    
    /* מניעת מריחת כפתורים וסידורם מימין לשמאל */
    .stButton>button {{
        width: auto !important;
        min-width: 140px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        transition: all 0.3s;
    }}
    
    .stButton>button:hover {{
        border-color: #ff4b4b;
        color: #ff4b4b;
    }}

    /* סידור אלמנטים של בחירה (Selectbox) */
    div[data-baseweb="select"] {{
        direction: rtl;
    }}

    /* עיצוב כותרות */
    h1, h2, h3, h4, p, span {{
        text-align: right !important;
        direction: rtl !important;
    }}

    /* הסתרת תפריטים מובנים של סטרימליט למראה נקי */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

def show_footer(version_label):
    """מציג קרדיט וגרסה בתחתית הדף"""
    st.markdown("---")
    st.caption(f"מתווך בקליק | גרסה {version_label} | הכנה למבחן המתווכים 2026")
