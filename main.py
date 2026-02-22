# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V101 | Date: 23/02/2026 | 00:35
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
    
    div.element-container { margin-bottom: 0px !important; padding-bottom: 0px !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0rem !important; }

    .header-box {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }

    /* מרכוז רשימת ההוראות מתחת לכותרת */
    .instructions-wrapper {
        text-align: center;
        width: 100%;
        margin-top: 10px;
    }
    .instructions-content {
        display: inline-block;
        text-align: right;
    }

    .q-text { font-size: 1.3rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; }
    
    /* העלאת פריים הניווט והטיימר למעלה */
    div[data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] {
        margin-top: -45px !important;
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

# 1. סטריפ עליון (2:1:2)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem; padding-left: 10px;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold; padding-right: 10px;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. כותרת
is_inst = ("step" not in st.session_state or st.session_state.step == "instructions")
t_val = "הוראות למבחן רישויי" if is_inst else "מבחן רישוי למתווכים"

_, title_mid, _ = st.columns([1, 2, 1])
with title_mid:
    st.markdown(f'<h1 style="text-align: center; font-size: 2.2rem; margin: 0; line-height: 1.1;">{t_val}</h1>', unsafe_allow_html=True)
    if not is_inst:
        st.markdown(f'<div style="text-align: center; color: #888; font-weight: bold; font-size: 1.1rem;">שאלה {st.session_state.current_q}</div>', unsafe_allow_html=True)

# 3. תוכן
if is_inst:
    st.markdown('<div class="instructions-wrapper"><div class="instructions-content">', unsafe_allow_html=True)
    instructions = [
        "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
        "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
        "ציון עובר: 60.", "שימוש במחשבון מותר.", "חל איסור על שימוש בחומר עזר."
    ]
    for i, txt in enumerate(instructions, 1):
        st.write(f"{i}. {txt}")
    st.markdown('</div></div>', unsafe_allow_html=True)
    
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
                el.innerHTML = (m < 10 ? '0
