# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V100 | Date: 23/02/2026 | 00:15
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
        max-width: 1050px !important; 
        margin: 0 auto !important; 
        padding-top: 0.5rem !important; 
    }
    
    /* צמצום רווחים בין אלמנטים */
    div.element-container { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0rem !important; }

    .header-box {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }

    /* יישור הוראות למרכז */
    .instructions-container {
        display: table;
        margin: 0 auto;
        text-align: right;
    }

    .q-text { font-size: 1.3rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; }
    
    /* העלאת פריים הניווט למעלה */
    [data-testid="column"]:nth-of-type(1) {
        margin-top: -15px !important;
    }

    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 10px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון
header_col_right, header_col_mid, header_col_left = st.columns([2, 1, 2])
with header_col_right:
    st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem; padding-left: 10px;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with header_col_mid:
    st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with header_col_left:
    st.markdown(f'<div style="text-align: right; font-weight: bold; padding-right: 10px;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. כותרת הדף
is_inst = ("step" not in st.session_state or st.session_state.step == "instructions")
t_val = "הוראות למבחן רישויי" if is_inst else "מבחן רישוי למתווכים"

_, title_mid, _ = st.columns([1, 2, 1])
with title_mid:
    st.markdown(f'<h1 style="text-align: center; font-size: 2.2rem; margin: 0; line-height: 1.1;">{t_val}</h1>', unsafe_allow_html=True)
    if not is_inst:
        st.markdown(f'<div style="text-align: center; color: #888; font-weight: bold; font-size: 1.1rem;">שאלה {st.session_state.current_q}</div>', unsafe_allow_html=True)

# 3. תוכן הדף
if is_inst:
    st.write("")
    st.markdown('<div class="instructions-container">', unsafe_allow_html=True)
    instructions = [
        "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
        "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
        "ציון עובר: 60.", "שימוש במחשבון מותר.", "חל איסור על שימוש בחומר עזר."
    ]
    for i, txt in enumerate(instructions, 1):
        st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;{i}. {txt}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    c1, c2 = st.columns([1, 1])
    with c1: agree = st.checkbox("קראתי את ההוראות")
    with c2:
        if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
            logic.start_exam_logic()
            st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    def get_timer_html():
        return f"""
        <div id="t-disp" style="text-align: center; background: #fff; border: 2px solid #333; padding: 5px; border-radius: 8px; font-weight: bold; font-size: 1.4rem; color: #333; font-family: monospace;"></div>
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

    col_nav, col_main = st.columns([1, 2.8], gap="medium")
    with col_nav:
        components.html(get_timer_html(), height=65)
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
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
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: 
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            st.divider()
            bn, bp, bf = st.columns([1, 1, 1])
            with bn:
                if st.session_state.current_q < 25:
                    if st.button("לשאלה הבאה", disabled=(choice is None), key="next"):
                        logic.move_to_next(); st.rerun()
            with bp:
                if st.button("לשאלה הקודמת", disabled=(st.session_state.current_q == 1), key="prev"):
                    st.session_state.current_q -= 1; st.rerun()
            with bf:
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="finish")

# סוף קובץ
