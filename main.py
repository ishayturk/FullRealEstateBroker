# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V50 | Date: 22/02/2026 | 17:00
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
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
        text-align: center;
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
    .q-header-text {
        color: #888; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px;
    }
    .q-text {
        font-size: 1.25rem; font-weight: bold; line-height: 1.5; margin-bottom: 15px; color: #000;
    }
    div[data-testid="stMarkdownContainer"] p { font-size: 1.1rem; }
    .centered-title { text-align: center; width: 100%; }
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
        st.markdown('<h1 class="centered-title">הוראות למבחן רישויי מקרקעין</h1>', unsafe_allow_html=True)
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "בסיום 90 דקות המבחן יינעל.", "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."]
        for i, txt in enumerate(instructions, 1):
            st.write(f"{i}. {txt}")
        
        st.write("")
        row_col1, row_col2 = st.columns([2.5, 1])
        with row_col1: agree = st.checkbox("קראתי את ההוראות")
        with row_col2:
            is_ready = logic.is_first_question_ready()
            if st.button("התחל בחינה", disabled=not (agree and is_ready)):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        st.markdown('<div class="nav-panel">', unsafe_allow_html=True)
        
        # שימוש במיכל ריק עבור השעון כדי לעדכן רק אותו
        timer_placeholder = st.empty()
        time_str = logic.get_remaining_time_str()
        timer_placeholder.markdown(f'<div class="timer-display">{time_str}</div>', unsafe_allow_html=True)
        
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.nav_active_questions
                    if cols[i].button(str(idx), key=f"nav_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div class="centered-title"><h2>מבחן רישוי למתווכים</h2></div>', unsafe_allow_html=True)
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p class="q-header-text">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"radio_{st.session_state.current_q}", label_visibility="collapsed")
            
            if choice:
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider()
            b_next, b_prev, b_finish = st.columns(3)
            with b_next:
                if st.button("לשאלה הבאה", disabled=(choice is None), key="btn_next"):
                    logic.move_to_next()
                    st.rerun()
            with b_prev:
                if st.button("לשאלה הקודמת", disabled=(st.session_state.current_q == 1), key="btn_prev"):
                    st.session_state.current_q -= 1
                    st.rerun()
            with b_finish:
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="btn_finish_active")

# סוף קובץ
