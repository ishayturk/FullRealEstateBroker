# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V146 | Date: 23/02/2026 | 15:55
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- 1. מגזר כללי --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 15px; }
    
    /* מפת מספרים - ספרות נקיות בלבד */
    .nav-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; text-align: center; }
    .nav-num { 
        cursor: pointer; 
        text-decoration: none !important; 
        color: #000; 
        font-size: 1.2rem; 
        border: none !important;
        background: none !important;
    }
    .nav-num.active { color: #007bff !important; font-weight: bold; font-size: 1.4rem; }
    .nav-num.disabled { color: #ccc !important; cursor: default; pointer-events: none; }

    /* עיצוב כותרת ושעון בשורה אחת */
    .exam-header-row { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        width: 100%; 
        margin-bottom: 20px;
    }
    .timer-display { font-size: 1.4rem; font-family: monospace; font-weight: bold; color: #333; }

    /* --- 2. מגזר מחשב (Desktop) --- */
    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 20px !important;
        }
        .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; color: #000; }
        .exam-title { font-size: 1.8rem; font-weight: bold; margin: 0; }
    }

    /* --- 3. מגזר נייד (Mobile) --- */
    @media (max-width: 768px) {
        div[data-testid="column"]:nth-of-type(1) { display: none !important; }
        div[data-testid="column"]:nth-of-type(2) { width: 100% !important; }
        .exam-header-row { flex-direction: column-reverse; gap: 10px; }
        .exam-title { font-size: 1.4rem !important; text-align: center; width: 100%; }
        
        /* קיצור טקסט כפתורים בנייד */
        button[key="next"] p { font-size: 0 !important; }
        button[key="next"] p::before { content: "הבאה"; font-size: 1rem; }
        button[key="prev"] p { font-size: 0 !important; }
        button[key="prev"] p::before { content: "הקודמת"; font-size: 1rem; }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# סטריפ עליון (מעוגן V113)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown(f'<div style="text-align: center; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)
with h3: 
    if st.button("חזרה", key="back_btn"):
        st.session_state.step = "instructions"
        st.rerun()
st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        st.write("1. המבחן כולל 25 שאלות.")
        st.write("2. זמן מוקצב: 90 דקות.")
        st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
        st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
        st.write("5. ציון עובר: 60.")
        if st.button("התחל בחינה", disabled=not logic.is_first_question_ready()):
            logic.start_exam_logic(); st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    timer_html = f"""
    <div id="t" class="timer-display" style="text-align: left;"></div>
    <script>
    var s = {rem_sec};
    function u() {{
        var m = Math.floor(s / 60); var sec = s % 60;
        var el = document.getElementById('t');
        if (el) {{
            if (s <= 600) el.style.color = "red";
            el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
        }}
        if (s > 0) s--;
    }}
    u(); setInterval(u, 1000);
    </script>
    """

    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        st.markdown('<p style="font-weight:bold;">מפת שאלות</p>', unsafe_allow_html=True)
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
        # שורת כותרת ושעון (שעון משמאל, כותרת מימין/מרכז)
        st.markdown('<div class="exam-header-row">', unsafe_allow_html=True)
        c_time, c_title = st.columns([1, 3])
        with c_time: components.html(timer_html, height=40)
        with c_title: st.markdown('<h2 class="exam-title">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            st.divider()
            
            bn, bp, bf = st.columns(3)
            with bn:
                if st.session_state.current_q < 25:
                    if st.button("השאלה הבאה", key="next", disabled=(choice is None)):
                        logic.move_to_next(); st.rerun()
            with bp:
                if st.session_state.current_q > 1:
                    if st.button("השאלה הקודמת", key="prev"):
                        st.session_state.current_q -= 1; st.rerun()
            with bf:
                if 25 in st.session_state.answers_user: st.button("סיום", key="finish")

# סוף קובץ
