# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V126 | Date: 22/02/2026 | 23:59
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
        max-width: 850px !important; 
        margin: 0 auto !important; 
        padding-top: 0rem !important; 
    }
    
    .header-box { border-bottom: 1px solid #eee; margin-top: 2px; margin-bottom: 5px; }

    .flex-header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; padding: 5px 0;
    }

    /* כותרת משולבת שעון */
    .title-row {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; margin: 0; padding: 0;
    }
    .title-row h2 { margin: 0 !important; font-size: 1.5rem !important; flex: 1; }
    .timer-container { min-width: 100px; text-align: left; }

    @media (max-width: 768px) {
        .mobile-spacer { height: 50px; }
        .title-row { flex-direction: column; text-align: center; gap: 5px; }
        .title-row h2 { font-size: 1.2rem !important; text-align: center !important; }
        .timer-container { text-align: center; width: 100%; }
    }

    /* צמצום רווחים בתוך השאלה */
    div[data-testid="stRadio"] > label { display: none; } /* הסתרת תווית רדיו מיותרת */
    div[data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    .stDivider { margin: 0.3rem 0 !important; }
    
    /* עיצוב מספרים לניווט - דחוס */
    .nav-num-wrapper {
        display: flex; flex-wrap: wrap; justify-content: center;
        gap: 10px; margin-top: 5px; padding: 5px;
    }
    div[data-testid="stHorizontalBlock"] button {
        background: none !important; border: none !important; padding: 0 !important;
        color: #007bff !important; text-decoration: underline;
        font-size: 0.95rem !important; min-width: auto !important;
    }
    div[data-testid="stHorizontalBlock"] button:disabled {
        color: #000 !important; text-decoration: none !important; cursor: default !important;
    }

    .q-text { font-size: 1.2rem; font-weight: bold; line-height: 1.2; margin-bottom: 5px; }
    
    /* מרכוז הוראות */
    .instructions-box {
        text-align: center; margin: 0 auto; max-width: 600px; line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="mobile-spacer"></div>', unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (עוגן V120)
st.markdown(f"""
    <div class="flex-header">
        <div style="text-align: left; flex: 1;">🏠 מתווך בקליק</div>
        <div style="text-align: center; color: #eee; flex: 0.2;">|</div>
        <div style="text-align: right; flex: 1;">👤 {user_name}</div>
    </div>
    <div class="header-box"></div>
""", unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<div class="instructions-box">', unsafe_allow_html=True)
    st.markdown('<h2>הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    st.write("המבחן כולל 25 שאלות. זמן מוקצב: 90 דקות.")
    st.write("מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("ציון עובר: 60. חל איסור על שימוש בחומר עזר.")
    
    st.write("")
    agree = st.checkbox("קראתי את ההוראות")
    if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
        logic.start_exam_logic()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    timer_js = f"""
    <div id="t-disp" style="font-weight: bold; font-family: monospace; color: #333; font-size: 1.2rem; display: inline-block;"></div>
    <script>
    var s = {rem_sec};
    function u() {{
        var m = Math.floor(s / 60); var sec = s % 60;
        var el = document.getElementById('t-disp');
        if (el) {{
            if (s <= 600) el.style.color = "red";
            el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
        }}
        if (s > 0) s--;
    }}
    u(); setInterval(u, 1000);
    </script>
    """

    # שורת כותרת ושעון מאוחדת
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        st.markdown('<h2 style="margin:0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
    with t_col2:
        components.html(timer_js, height=35)

    q = st.session_state.exam_data.get(st.session_state.current_q)
    if q:
        st.markdown(f'<p style="color: #888; font-weight: bold; margin: 0;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
        
        prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
        choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
        if choice is not None: 
            st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
        
        st.divider()
        
        # כפתורי ניווט
        bn, bp, bf = st.columns(3)
        with bn:
            if st.session_state.current_q < 25:
                if st.button("לשאלה הבאה ⬅️", disabled=(choice is None), use_container_width=True):
                    logic.move_to_next(); st.rerun()
        with bp:
            if st.button("➡️ לשאלה הקודמת", disabled=(st.session_state.current_q == 1), use_container_width=True):
                st.session_state.current_q -= 1; st.rerun()
        with bf:
            if 25 in st.session_state.answers_user:
                st.button("סיום בחינה ✅", key="finish", use_container_width=True)

        # מפת מספרים דחוסה למטה
        st.markdown('<div class="nav-num-wrapper">', unsafe_allow_html=True)
        num_cols = st.columns(25)
        for i in range(1, 26):
            with num_cols[i-1]:
                is_active = i in st.session_state.nav_active_questions
                if st.button(str(i), key=f"map_{i}", disabled=not is_active):
                    st.session_state.current_q = i; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# סוף קובץ
