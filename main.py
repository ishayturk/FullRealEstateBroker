# ==========================================
# Project: מתווך בקליק | File: main.py
# Version: 1218-G2 | Anchor: 1218-G2
# ==========================================
import streamlit as st
from logic import initialize_exam, fetch_next_question

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם המשתמש מהכתובת
user_name = st.query_params.get("user", "אורח")

# 2. הלינק המדויק לאפליקציית הלימוד שסיפקת
study_app_url = "https://ishayturk-realtor-app-app-kk1gme.streamlit.app/"
# יצירת הכתובת המלאה לחזרה עם הפרמטר
back_url = f"{study_app_url}?user={user_name.replace(' ', '%20')}"

# CSS לעיצוב הסטריפ והוראות המבחן
st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .top-strip {{
        position: relative;
        top: 10px; 
        width: 100%;
        height: 50px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 25px;
        direction: rtl;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 15px;
    }}
    
    .strip-right {{
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    
    .strip-logo {{ 
        font-weight: bold; 
        font-size: 1.2rem; 
        color: #31333f;
    }}
    
    .strip-user {{ 
        font-weight: 900 !important;
        font-size: 1.1rem; 
        display: flex;
        align-items: center;
        gap: 8px;
        color: #31333f;
    }}
    
    .back-btn-active {{
        text-decoration: none !important;
        color: #31333f !important;
        border: 1px solid #d1d5db !important;
        padding: 6px 18px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: 0.2s;
        display: inline-block;
        font-size: 0.9rem;
    }}
    
    .back-btn-active:hover {{
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
        background-color: #fffafa !important;
    }}

    .block-container {{
        direction: rtl;
        max-width: 800px;
        margin: auto;
        padding-top: 0px !important;
    }}
    
    h1 {{ 
        font-size: 2rem !important; 
        margin-top: 0px !important; 
        margin-bottom: 15px
