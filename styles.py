# Project: מתווך בקליק | Version: B01
# File: styles.py
import streamlit as st

def apply_styles(version_name="B01"):
    st.markdown(f"""
    <style>
        * {{ direction: rtl; text-align: right; }}
        .stButton>button {{ width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }}
        .top-link {{ 
            display: inline-block; width: 100%; text-align: center; 
            border-radius: 8px; text-decoration: none; border: 1px solid #d1d5db;
            font-weight: bold; height: 2.8em; line-height: 2.8em;
            background-color: transparent; color: inherit;
        }}
        .v-footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.1); /* לבן שקוף מאוד */
            font-size: 0.7em;
            margin-top: 50px;
            width: 100%;
        }}
        [data-testid="stSidebar"] {{ display: none; }}
    </style>
    <div id="top"></div>
    """, unsafe_allow_html=True)

def show_footer(version_name="B01"):
    st.markdown(f'<div class="v-footer">Version: {version_name}</div>', unsafe_allow_html=True)
