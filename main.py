# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V174 | Date: 24/02/2026 | 01:40
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- SECTION: GENERAL --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 15px; }
    .stDivider { margin: 0.5rem 0 !important; }
    .nav-title { margin-top: -10px !important; margin-bottom: 5px !important; display: block; }
    
    /* --- SECTION: DESKTOP --- */
    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 15px !important;
        }
        .q-text { font-size: 1.25rem !important; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
    }

    /* --- SECTION: MOBILE --- */
    @media (max-width: 768px) {
        div[data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] {
            gap: 0rem !important;
            margin-top: 0px !important;
            padding-top: 0px !important;
        }
        .q-text { font-size: 1.25rem !important; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון
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
    rem_sec = logic.get_remaining_seconds()
    
    # כותרת ושעון בתוך בלוק HTML אחד למניעת שבירת שורה
    combined_html = f"""
    <div style="direction: rtl; display: flex; align-items: center; justify-content: center; width: 100%; white-space: nowrap;">
        <style>
            /* מצב מחשב */
            .t-title {{ font-size: 3.0rem; font-weight: bold; font-family: sans-serif; color: #000; margin: 0; }}
            .t-clock {{ font-size: 2.2rem; font-weight: bold; font-family: monospace; color: #333; margin-right: 30px; }}
            
            /* מצב נייד */
            @media (max-width: 768px) {{
                .t-title {{ font-size: 1.1rem !important; }}
                .t-clock {{ font-size: 1.0rem !important; margin-right: 15px !important; }}
            }}
        </style>
        <div class="t-title">מבחן רישוי למתווכים</div>
        <div id="clock-val" class="t-clock" style="direction: ltr;"></div>
    </div>
    <script>
    var s = {rem_sec};
    function u() {{
        var m = Math.floor(s / 60); var sec = s % 60;
        var el = document.getElementById('clock-val');
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
        st.markdown('<b class="nav-title">מפת שאלות:</b>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.nav_active_questions
                    label = f"**{idx}**" if idx == st.session_state.current_q else str(idx)
                    if cols[i].button(label, key=f"n_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx; st.rerun()

    with col_main:
        # רכיב HTML אחד שתופס את כל הרוחב ומונע שבירת שורה
        components.html(combined_html, height=85)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom: 2px;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            st.divider()
            bn, bp, bf = st.columns(3)
            with bn:
                if st.session_state.current_q < 25:
                    if st.button("לשאלה הבאה", disabled=(choice is None), key="next"):
                        logic.move_to_next(); st.rerun()
            with bp:
                if st.button("לשאלה הקודמת", disabled=(st.session_state.current_q == 1), key="prev"):
                    st.session_state.current_q -= 1; st.rerun()
            with bf:
                if 25 in st.session_state.answers_user: st.button("סיום בחינה", key="finish")

# סוף קובץ
