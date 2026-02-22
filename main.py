# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V44 | Date: 22/02/2026 | 15:35
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
    }
    .header-style {
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .nav-panel { 
        background-color: #f8f9fa; 
        border: 1px solid #e1e4e8; 
        padding: 20px; 
        border-radius: 12px; 
    }
    .timer-display {
        text-align: center; background: #fff; border: 1px solid #333;
        padding: 8px; border-radius: 8px; font-weight: bold;
        font-size: 1.5rem; color: #333; margin-bottom: 15px; font-family: monospace;
    }
    .q-box-btn {
        width: 100%; height: 40px; border-radius: 5px; border: 1px solid #eee;
        background: #fff; color: #ccc; display: flex; align-items: center; 
        justify-content: center; margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

_, head_col, _ = st.columns([1, 4, 1])
with head_col:
    st.markdown('<div class="header-style">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1: st.markdown(f"<div style='text-align: right; font-size: 1.3rem;'>🏠 <b>מתווך בקליק</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='text-align: left; font-size: 1.2rem;'>👤 <b>{user_name}</b></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h1 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h1>', unsafe_allow_html=True)
        instructions = [
            "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.",
            "ניתן לחזור אחורה רק לשאלות שנענו.", "בסיום 90 דקות המבחן יינעל.",
            "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
        ]
        for i, txt in enumerate(instructions, 1):
            st.write(f"{i}. {txt}")
        
        st.write("")
        row_col1, row_col2 = st.columns([2.5, 1])
        with row_col1: agree = st.checkbox("קראתי את ההוראות")
        with row_col2:
            try: is_ready = logic.is_first_question_ready()
            except: is_ready = False
            if st.button("התחל בחינה", disabled=not (agree and is_ready)):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        st.markdown('<div class="nav-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="timer-display">90:00</div>', unsafe_allow_html=True)
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    cols[i].markdown(f'<div class="q-box-btn">{idx}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div style="text-align: center;"><h2 style="margin:0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #555;">שאלה {st.session_state.current_q} מתוך 25</p></div>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f"#### {q['question']}")
            # בחירת תשובה מעדכנת את הזיכרון
            choice = st.radio("בחר תשובה:", q["options"], index=None, key=f"radio_{st.session_state.current_q}")
            if choice:
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider()
            # סדר כפתורים: הבא (ימין), הקודם (מרכז), סיום (שמאל - מותנה)
            b_next, b_prev, b_finish = st.columns(3)
            with b_next:
                st.button("לשאלה הבאה", disabled=True, key="btn_next_dummy")
            with b_prev:
                st.button("לשאלה הקודמת", disabled=True, key="btn_prev_dummy")
            with b_finish:
                # כפתור סיום מופיע רק אם המשתמש ענה על שאלה 25
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="btn_finish_active")

# סוף קובץ
