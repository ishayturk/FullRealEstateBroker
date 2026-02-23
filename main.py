# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V147 | Date: 23/02/2026 | 16:30
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    
    .block-container { 
        max-width: 1100px !important; 
        margin: 0 auto !important; 
        padding-top: 0.5rem !important; 
    }
    
    .header-box {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    /* יישור פריים הניווט */
    div[data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
        margin-top: 0px !important;
        padding-top: 0px !important;
    }

    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 15px !important;
        }
    }

    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
    .stDivider { margin: 0.5rem 0 !important; }
    .nav-title { margin-top: -10px !important; margin-bottom: 5px !important; display: block; }

    /* עיצוב שורת כותרת ושעון */
    .exam-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .timer-display {
        font-size: 1.3rem;
        font-family: monospace;
        font-weight: bold;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (2:1:2)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(
