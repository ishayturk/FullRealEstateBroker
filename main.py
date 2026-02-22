# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V69 | Date: 22/02/2026 | 22:45
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    
    /* מרווח עליון מינימלי למניעת חסימת הסטריפ המערכתי */
    .block-container { 
        max-width: 1100px !important; 
        margin: 0 auto !important; 
        padding-top: 0.5rem !important; 
    }
    
    /* Header - ברירת מחדל (דסקטופ) */
    .header-style { border-bottom: 2px solid #f0f0f0; padding-bottom: 8px; margin-bottom: 15px; }
    .header-content { display: flex; justify-content: space-between; align-items: center; }
    .header-logo { font-size: 1.3rem; font-weight: bold; }
    .header-user { font-size: 1.1rem; color: #666; }

    /* דף הסבר - ריווח ימני בנייד */
    .instruction-wrapper { padding-right: 30px; line-height: 1.4; }

    @media (max-width: 768px) {
        /* כיווץ ה-Header לשורה אחת בנייד */
        .header-logo { font-size: 1rem !important; }
        .header-user { font-size: 0.9rem !important; }
        
        /* הסתרת מפת השאלות בנייד - השארת הפריים רק עבור השעון */
        div[data-testid="column"]:nth-of-type(1) .stButton { display: none !important; }
        div[data-testid="column"]:nth-of-type(1) b { display: none !important; }
        
        /* צמצום רווחים בנייד */
        .block-container { padding-right: 10px !important; padding-left: 10px !important; }
    }

    @media (min-width: 769px) {
        /* פריים ניווט דסקטופ - העלאת התוכן למעלה */
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 10px !important; /* צמצום פדינג */
        }
    }

    /* הידוק רכיבי השאלה */
    .q-text { font-size: 1.2rem; font-weight: bold; margin-bottom: 8px; line-height: 1.3; }
    .stDivider { margin: 0.4rem 0 !important; }
    .stRadio > div { gap: 0.3rem !important; }
    </style>
""", unsafe_allow_html=True)

# הצגת Header - שורה אחת תמיד
st.markdown(f"""
    <div class="header-style">
        <div class="header-content">
            <div class="header-logo">🏠 מתווך בקליק</div>
            <div class="header-user">👤 {user_name}</div>
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
    
    def get_timer_html(font_size, padding="10px"):
        return f"""
        <div id="timer-display" style="text-align: center; background: #fff; border: 2px solid #333; padding: {padding}; border-radius: 8px; font-weight: bold; font-size: {font_size}; color: #333; font-family: monospace;"></div>
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

    # חלוקה לעמודות - בנייד הן יופיעו אחת מעל השנייה (שעון מעל שאלה)
    col_nav, col_main = st.columns([1, 2.8], gap="small")
    
    with col_nav:
        # השעון יופיע גם בנייד וגם במחשב (בנייד הוא יקטן ב-HTML)
        timer_size = "1.6rem" if st.query_params.get("mobile") != "true" else "1.1rem"
        components.html(get_timer_html(timer_size, "5px"), height=65)
        
        # מפת שאלות - תוסתר בנייד דרך ה-CSS למעלה
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 5): # 5 בשורה לצמצום גובה
            cols = st.columns(5)
            for i in range(5):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.nav_active_questions
                    if cols[i].button(str(idx), key=f"nav_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx
                        st.rerun()

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
                if st.button("הבא", disabled=(choice is None), key="btn_next"):
                    logic.move_to_next()
                    st.rerun()
            with b_prev:
                if st.button("הקודם", disabled=(st.session_state.current_q == 1), key="btn_prev"):
                    st.session_state.current_q -= 1
                    st.rerun()
            with b_finish:
                if 25 in st.session_state.answers_user:
                    st.button("סיום", key="btn_finish_active")

# סוף קובץ
