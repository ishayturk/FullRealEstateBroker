# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V111 | Date: 22/02/2026 | 21:50
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
        max-width: 1100px !important; 
        margin: 0 auto !important; 
        padding-top: 0.5rem !important; 
    }
    
    .header-box {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    /* מרכוז אבסולוטי של בלוק ההוראות */
    .inst-outer {
        text-align: center;
        width: 100%;
        margin: 20px 0;
    }
    .inst-inner {
        display: inline-block;
        text-align: right;
    }

    /* יישור פריים הניווט */
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

# 1. סטריפ עליון (2:1:2)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center; margin-bottom: 10px;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    
    # גוף ההוראות הממורכז
    st.markdown('<div class="inst-outer"><div class="inst-inner">', unsafe_allow_html=True)
    instructions = [
        "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
        "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
        "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
    ]
    for i, txt in enumerate(instructions, 1):
        st.write(f"{i}. {txt}")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.write("")
    # שורה תחתונה - מרכוז וסגירת רווחים
    _, footer_row, _ = st.columns([0.5, 2, 0.5])
    with footer_row:
        f_c1, f_c2 = st.columns([1.2, 1])
        with f_c1: agree = st.checkbox("קראתי את ההוראות")
        with f_c2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    def get_timer_html():
        return f"""
        <div id="t-disp" style="text-align: center; background: #fff; border: 2px solid #333; padding: 8px; border-radius: 8px; font-weight: bold; font-size: 1.5rem; color: #333; font-family: monospace;"></div>
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

    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        components.html(get_timer_html(), height=70)
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
        st.markdown('<h2 style="text-align: center; margin-top: 0; padding-top: 0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom: 5px;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: 
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
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
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="finish")

# סוף קובץ
