# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V59 | Date: 22/02/2026 | 20:10
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 1rem !important; }
    .header-style { border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 20px; text-align: center; }
    
    /* הגדרות לשעון הנייד - מוסתר בדסקטופ */
    .mobile-timer-area { display: none; }

    @media (max-width: 768px) {
        /* הסתרת פריים הניווט בנייד */
        [data-testid="column"]:nth-child(1) { display: none !important; }
        /* הצגת אזור השעון בנייד */
        .mobile-timer-area { display: block; margin-bottom: 15px; }
    }

    @media (min-width: 769px) {
        /* עיצוב פריים ניווט אפור בדסקטופ */
        [data-testid="column"]:nth-child(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 20px !important;
        }
    }

    .q-header-text { color: #888; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px; }
    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.5; margin-bottom: 15px; color: #000; }
    div[data-testid="stMarkdownContainer"] p { font-size: 1.1rem; }
    .centered-title { text-align: center; width: 100%; }
    </style>
""", unsafe_allow_html=True)

_, head_col, _ = st.columns([1, 4, 1])
with head_col:
    st.markdown('<div class="header-style">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1: st.markdown(f"<div style='text-align: right; font-size: 1.3rem;'>🏠 <b>מתווך בקליק</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div style='text-align: left; font-size: 1.2rem;'>👤 <b>{user_name}</b></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h1 class="centered-title">הוראות למבחן רישויי מקרקעין</h1>', unsafe_allow_html=True)
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "בסיום 90 דקות המבחן יינעל.", "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.write("")
        row_col1, row_col2 = st.columns([2.5, 1])
        with row_col1: agree = st.checkbox("קראתי את ההוראות")
        with row_col2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    # פונקציה לייצור השעון עם גמישות בגודל
    def get_timer_html(font_size="1.7rem", padding="10px"):
        return f"""
        <div id="timer-display" style="text-align: center; background: #fff; border: 2px solid #333; padding: {padding}; border-radius: 8px; font-weight: bold; font-size: {font_size}; color: #333; font-family: monospace;"></div>
        <script>
        var seconds = {rem_sec};
        function update() {{
            var m = Math.floor(seconds / 60);
            var s = seconds % 60;
            var el = document.getElementById('timer-display');
            if (seconds <= 600) {{ el.style.color = "red"; }}
            el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
            if (seconds > 0) seconds--;
        }}
        update(); setInterval(update, 1000);
        </script>
        """

    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        # שעון דסקטופ (גדול)
        components.html(get_timer_html("1.7rem", "10px"), height=85)
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
        # אזור שעון נייד (קטן) - נשלט ע"י CSS
        st.markdown('<div class="mobile-timer-area">', unsafe_allow_html=True)
        components.html(get_timer_html("1.1rem", "5px"), height=50)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="centered-title"><h2>מבחן רישוי למתווכים</h2></div>', unsafe_allow_html=True)
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p class="q-header-text">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"radio_{st.session_state.current_q}", label_visibility="collapsed")
            if choice: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            st.divider()
            b_next, b_prev,
