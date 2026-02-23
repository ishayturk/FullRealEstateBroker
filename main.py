# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V141 | Date: 23/02/2026 | 13:50
import streamlit as st
import logic

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- 1. מגזר כללי --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 15px; }
    
    /* עיצוב מפת המספרים */
    .nav-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; text-align: center; }
    .nav-num { padding: 8px 5px; cursor: pointer; border-radius: 4px; border: 1px solid #ddd; display: block; text-decoration: none; color: #333; font-size: 0.9rem; }
    .nav-num.active { background-color: #007bff; color: white !important; font-weight: bold; border-color: #0056b3; }
    .nav-num.disabled { color: #ccc; cursor: default; border-color: #eee; pointer-events: none; }

    /* --- 2. מגזר מחשב (Desktop - V113 Style) --- */
    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 15px !important;
        }
        .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
        .nav-title { margin-top: 0px; margin-bottom: 10px; display: block; font-weight: bold; }
    }

    /* --- 3. מגזר נייד (Mobile - Clean Start) --- */
    @media (max-width: 768px) {
        div[data-testid="column"]:nth-of-type(1) {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="column"]:nth-of-type(2) { width: 100% !important; }
        h2 { font-size: 1.2rem !important; }
        .q-text { font-size: 1.1rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (V113)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.write("")
        f_c1, f_c2 = st.columns([1, 1])
        with f_c1: agree = st.checkbox("קראתי את ההוראות")
        with f_c2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic(); st.rerun()

elif st.session_state.step == "exam_run":
    # ניווט דרך URL (למפת המספרים)
    q_param = st.query_params.get("q")
    if q_param and int(q_param) != st.session_state.current_q:
        st.session_state.current_q = int(q_param)
        st.rerun()

    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        st.markdown('<p class="nav-title">מפת שאלות</p>', unsafe_allow_html=True)
        # בניית מפת מספרים לחיצה
        html_grid = '<div class="nav-grid">'
        for i in range(1, 26):
            is_active = i in st.session_state.nav_active_questions
            is_current = (i == st.session_state.current_q)
            cls = "nav-num"
            if is_current: cls += " active"
            elif not is_active: cls += " disabled"
            html_grid += f'<a class="{cls}" href="?q={i}" target="_self">{i}</a>'
        html_grid += '</div>'
        st.markdown(html_grid, unsafe_allow_html=True)

    with col_main:
        st.markdown('<h2 style="text-align: center; margin-top: 0; padding-top: 0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom: 5px;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            st.divider()
            
            bn, bp, bf = st.columns(3)
            with bn:
                if st.session_state.current_q < 25:
                    if st.button("הבא", key="next", disabled=(choice is None)):
                        logic.move_to_next(); st.rerun()
            with bp:
                if st.button("הקודם", key="prev", disabled=(st.session_state.current_q == 1)):
                    st.session_state.current_q -= 1; st.rerun()
            with bf:
                if 25 in st.session_state.answers_user: st.button("סיום", key="finish")

# סוף קובץ
