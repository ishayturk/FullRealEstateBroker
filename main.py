# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V73 | Date: 22/02/2026 | 23:59
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
        padding-top: 1rem !important; 
    }
    
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        margin-bottom: 10px;
    }

    .instruction-box { padding-right: 25px; }

    @media (max-width: 768px) {
        div[data-testid="column"]:nth-of-type(1) { display: none !important; }
        .block-container { padding-right: 15px !important; padding-left: 15px !important; }
    }

    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 20px !important;
        }
    }

    .exam-title-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 5px;
    }
    .exam-title { 
        font-size: 1.4rem;
        font-weight: bold;
        text-align: center;
    }

    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
    .stDivider { margin: 0.5rem 0 !important; }
    
    .stButton > button[key="logo_link"] {
        background: none; border: none; padding: 0; color: black;
        font-size: 1.2rem; font-weight: bold; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container">', unsafe_allow_html=True)
h_left, h_right = st.columns([1, 1])
with h_left:
    if st.button("🏠 מתווך בקליק", key="logo_link"):
        st.session_state.step = "instructions"
        st.rerun()
with h_right:
    st.markdown(f'<div style="font-size: 1rem; color: #666; text-align: left;">👤 {user_name}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
        st.markdown('<div class="instruction-box">', unsafe_allow_html=True)
        # 7 הסעיפים המלאים מהמקור שלך
        instructions = [
            "המבחן כולל 25 שאלות.", 
            "זמן מוקצב: 90 דקות.", 
            "מעבר לשאלה הבאה רק לאחר סימון תשובה.", 
            "ניתן לחזור אחורה רק לשאלות שנענו.", 
            "ציון עובר: 60.", 
            "שימוש במחשבון מותר.",
            "חל איסור על שימוש בחומר עזר."
        ]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        row_col1, row_col2 = st.columns([2.5, 1])
        with row_col1: agree = st.checkbox("קראתי את ההוראות")
        with row_col2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    def get_timer_html(font_size):
        return f"""
        <div id="timer-display" style="text-align: center; background: #fff; border: 2px solid #333; padding: 10px; border-radius: 8px; font-weight: bold; font-size: {font_size}; color: #333; font-family: monospace;"></div>
        <script>
        var seconds = {rem_sec};
        function update() {{
            var m = Math.floor(seconds / 60);
            var s = seconds % 60;
            var el = document.getElementById('timer-display');
            if (el) {{
                if (seconds <= 600) {{ el.style.color = "red"; }}
                el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
            }}
            if (seconds > 0) seconds--;
        }}
        update(); setInterval(update, 1000);
        </script>
        """

    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        components.html(get_timer_html("1.7rem"), height=85)
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
