# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V72 | Date: 22/02/2026 | 23:30
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
    
    /* Header - מרכוז מלא */
    .header-style { 
        border-bottom: 2px solid #f0f0f0; 
        padding-bottom: 8px; 
        margin-bottom: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .header-group { display: flex; align-items: baseline; gap: 10px; }
    .header-logo { font-size: 1.25rem; font-weight: bold; color: #333; }
    .header-user { font-size: 1rem; color: #666; font-weight: normal; }

    /* דף הוראות - ריווח ימני */
    .instruction-wrapper { padding-right: 30px; line-height: 1.5; }

    @media (max-width: 768px) {
        .header-logo { font-size: 1.05rem !important; }
        .header-user { font-size: 0.85rem !important; }
        .desktop-nav-content { display: none !important; }
        .block-container { padding-right: 10px !important; padding-left: 10px !important; }
    }

    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 10px 5px !important;
        }
    }

    /* עיצוב מספרים במפה - ללא מראה כפתור מגושם */
    div.stButton > button {
        border: none !important;
        background: transparent !important;
        color: #444 !important;
        font-size: 1.1rem !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    div.stButton > button:disabled {
        color: #ccc !important;
        background: transparent !important;
    }
    div.stButton > button:hover {
        color: #000 !important;
        text-decoration: underline !important;
    }

    .q-text { font-size: 1.2rem; font-weight: bold; margin-bottom: 8px; line-height: 1.3; }
    .stDivider { margin: 0.3rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

# Header ממורכז
st.markdown(f"""
    <div class="header-style">
        <div class="header-group">
            <span class="header-logo">🏠 מתווך בקליק</span>
            <span class="header-user">| 👤 משתמש: {user_name}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h2 style="text-align: center; margin-top:0;">הוראות למבחן</h2>', unsafe_allow_html=True)
        st.markdown('<div class="instruction-wrapper">', unsafe_allow_html=True)
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("")
        row_col1, row_col2 = st.columns([2, 1])
        with row_col1: agree = st.checkbox("קראתי את ההוראות")
        with row_col2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    def get_timer_html(font_size):
        return f"""
        <div id="timer-display" style="text-align: center; background: #fff; border: 2px solid #333; padding: 5px; border-radius: 8px; font-weight: bold; font-size: {font_size}; color: #333; font-family: monospace;"></div>
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

    col_nav, col_main = st.columns([1, 3], gap="small")
    
    with col_nav:
        # שעון
        timer_size = "1.4rem" if st.query_params.get("mobile") != "true" else "1.1rem"
        components.html(get_timer_html(timer_size), height=50)
        
        # מפת שאלות - מספרים בלבד לפי הפרוטוקול
        st.markdown('<div class="desktop-nav-content">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; font-weight:bold; margin-bottom:5px;">מפת שאלות:</div>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    # שאלה פעילה רק אם היא הנוכחית או כבר נענתה (לפי הפרוטוקול)
                    is_active = idx in st.session_state.nav_active_questions
                    label = f"**{idx}**" if idx == st.session_state.current_q else str(idx)
                    if cols[i].button(label, key=f"nav_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<h3 style="text-align: center; margin: 0;">מבחן רישוי</h3>', unsafe_allow_html=True)
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-size:0.9rem; margin-bottom:2px;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"radio_{st.session_state.current_q}", label_visibility="collapsed")
            if choice: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider()
            
            b_next, b_prev, b_finish = st.columns(3)
            with b_next:
                if st.button("לשאלה הבאה", disabled=(choice is None), key="btn_next", use_container_width=True):
                    logic.move_to_next()
                    st.rerun()
            with b_prev:
                if st.button("לשאלה הקודמת", disabled=(st.session_state.current_q == 1), key="btn_prev", use_container_width=True):
                    st.session_state.current_q -= 1
                    st.rerun()
            with b_finish:
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="btn_finish_active", use_container_width=True)

# סוף קובץ
