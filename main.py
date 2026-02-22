# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V65 | Date: 22/02/2026 | 21:35
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    
    /* מרווח מהסטריפ העליון המקורי של המערכת */
    .block-container { 
        max-width: 1100px !important; 
        margin: 0 auto !important; 
        padding-top: 2rem !important; 
    }
    
    /* עיצוב ה-Header הפנימי - מוקטן לנייד */
    .header-style { 
        border-bottom: 2px solid #f0f0f0; 
        padding-bottom: 10px; 
        margin-bottom: 20px; 
        text-align: center; 
    }
    .logo-row { font-size: 1.3rem; font-weight: bold; margin-bottom: 3px; color: #333; text-align: center; }
    .user-row { font-size: 1rem; color: #666; text-align: center; }

    /* שעון מובייל - מוסתר לחלוטין בדסקטופ */
    .mobile-only-timer { 
        display: none; 
        height: 0px !important; 
        margin: 0px !important; 
        overflow: hidden; 
    }

    @media (max-width: 768px) {
        /* ריווח מהצדדים בנייד */
        .block-container { padding-right: 20px !important; padding-left: 20px !important; }
        
        /* הסתרת עמודת הניווט (המפה והשעון הגדול) */
        div[data-testid="column"]:nth-of-type(1) { display: none !important; }
        
        /* הצגת השעון הקטן בנייד */
        .mobile-only-timer { 
            display: block !important; 
            height: auto !important; 
            margin-bottom: 15px !important; 
            overflow: visible !important;
        }
    }

    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 20px !important;
        }
    }

    .q-header-text { color: #888; font-weight: bold; font-size: 1.1rem; margin-bottom: 5px; }
    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.5; margin-bottom: 15px; color: #000; }
    .centered-title { text-align: center; width: 100%; margin-top: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# ה-Header הפנימי (מתחת לסטריפ הראשי)
st.markdown(f"""
    <div class="header-style">
        <div class="logo-row">🏠 מתווך בקליק</div>
        <div class="user-row">👤 {user_name}</div>
    </div>
""", unsafe_allow_html=True)

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
    
    def get_timer_html(id_tag, font_size, padding):
        return f"""
        <div id="{id_tag}" style="text-align: center; background: #fff; border: 2px solid #333; padding: {padding}; border-radius: 8px; font-weight: bold; font-size: {font_size}; color: #333; font-family: monospace;"></div>
        <script>
        var seconds = {rem_sec};
        function update() {{
            var m = Math.floor(seconds / 60);
            var s = seconds % 60;
            var el = document.getElementById('{id_tag}');
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
        components.html(get_timer_html("timer-desktop", "1.7rem", "10px"), height=85)
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
        st.markdown('<div class="mobile-only-timer">', unsafe_allow_html=True)
        components.html(get_timer_html("timer-mobile", "1.1rem", "5px"), height=50)
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
