# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V117 | Date: 22/02/2026 | 22:30
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; box-sizing: border-box; }
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

    /* התאמות לנייד */
    @media (max-width: 768px) {
        /* דחיקה למטה למניעת הסתרה */
        div[data-testid="stHorizontalBlock"]:first-of-type {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding-top: 45px !important;
        }
        
        h2 { font-size: 1.35rem !important; }
        
        .mobile-inst-padding {
            padding-right: 30px !important;
            padding-left: 10px !important;
            width: 100% !important;
        }

        /* הקטנת גופנים בסטריפ בנייד */
        div[data-testid="stHorizontalBlock"]:first-of-type div {
            font-size: 0.85rem !important;
        }
    }

    /* יישור פריים הניווט במחשב */
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
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (2:1:2) - חוזר למבנה עמודות יציב
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; white-space: nowrap;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold; white-space: nowrap;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown('<div class="mobile-inst-padding">', unsafe_allow_html=True)
        instructions = [
            "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
            "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
            "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
        ]
        for i, txt in enumerate(instructions, 1):
            st.write(f"{i}. {txt}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        f_c1, f_c2 = st.columns([1, 1])
        with f_c1:
            agree = st.checkbox("קראתי את ההוראות")
        with f_c2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    def get_timer_html():
        return f"""
        <div id="t-disp" style="text-align: center; background: #fff; border: 2px solid #333; padding: 8px; border-radius
