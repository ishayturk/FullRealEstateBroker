# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V67 | Date: 22/02/2026 | 22:10
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
    
    /* Header מקורי מהעוגן */
    .header-style { border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 20px; }
    
    /* רווח לימין בדף ההסבר */
    .instruction-box { padding-right: 25px; }

    @media (max-width: 768px) {
        /* ביטול פריים ניווט בנייד */
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

    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
    .stDivider { margin: 0.5rem 0 !important; } /* צמצום רווח Divider */
    </style>
""", unsafe_allow_html=True)

# Header מקורי (שורה אחת)
st.markdown('<div class="header-style">', unsafe_allow_html=True)
h_col1, h_col2 = st.columns([1, 1])
with h_col1:
    st.markdown(f'<div style="font-size: 1.3rem; font-weight: bold;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown(f'<div style="font-size: 1.1rem; color: #666; text-align: left;">👤 {user_name}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
        st.markdown('<div class="instruction-box">', unsafe_allow_html=True)
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."]
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
        # שעון דסקטופ בלבד
        components.html(get_timer_html("1.7rem"), height=85)
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

    with col_main:
        # בנייד - הצגת שעון קטן בראש השאלה בלבד (לא קיים במחשב)
        if st.columns([1])[0].button("", key="is_mobile_check", help="hidden"): pass # Dummy for detection
        
        st.markdown('<h2 style="text-align: center; margin-top: 0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"radio_{st.session_state.current_q}", label_visibility="collapsed")
            if choice: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider() # Divider מצומצם דרך CSS
            
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
