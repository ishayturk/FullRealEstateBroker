# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V78 | Date: 23/02/2026 | 01:25
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
    
    /* Header Container - רספונסיבי וממורכז לתוכן */
    .header-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        max-width: 1000px;
        margin: 0 auto 20px auto;
        padding: 10px 0;
    }

    /* התאמה לנייד */
    @media (max-width: 600px) {
        .header-wrapper {
            flex-direction: column;
            gap: 10px;
            text-align: center;
        }
    }

    .logo-link-style {
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        color: black;
        cursor: pointer;
    }

    .exam-header-box {
        text-align: center;
        margin: 0 auto 30px auto;
        width: 100%;
    }
    .exam-title { 
        font-size: 2.2rem;
        font-weight: bold;
        display: inline-block;
        border-bottom: 2px solid #333;
        padding-bottom: 5px;
        margin-bottom: 8px;
    }
    .q-id { color: #888; font-size: 1.1rem; font-weight: bold; }

    /* ניווט - מניעת שבירת טקסט בכפתורים */
    div[data-testid="column"] button {
        white-space: nowrap !important;
        min-width: 42px !important;
        padding: 2px 5px !important;
    }

    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 20px !important;
        }
    }

    .q-text { font-size: 1.3rem; font-weight: bold; line-height: 1.4; margin-bottom: 15px; color: #000; }
    .stDivider { margin: 1rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

# הצגת Header ללא Columns של Streamlit
st.markdown(f"""
    <div class="header-wrapper">
        <div class="logo-link-style">🏠 מתווך בקליק</div>
        <div style="font-size: 1rem; color: #666;">👤 {user_name}</div>
    </div>
""", unsafe_allow_html=True)

# כפתור שקוף מעל הלוגו בשביל הפונקציונליות של Streamlit
st.markdown('<div style="position: absolute; top: 15px; right: 50px; opacity: 0;">', unsafe_allow_html=True)
if st.button("back", key="logo_link"):
    st.session_state.step = "instructions"
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
        st.markdown('<div style="padding-right: 25px;">', unsafe_allow_html=True)
        instructions = [
            "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
            "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
            "ציון עובר: 60.", "שימוש במחשבון מותר.", "חל איסור על שימוש בחומר עזר."
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

    col_nav, col_main = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        components.html(get_timer_html("1.7rem"), height=85)
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.nav_active_questions
                    label = f"**{idx}**" if idx == st.session_state.current_q else str(idx)
                    if cols[i].button(label, key=f"nav_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx
                        st.rerun()

    with col_main:
        # כותרת ומזהה שאלה במבנה ממורכז ומהודק
        st.markdown(f"""
            <div class="exam-header-box">
                <div class="exam-title">מבחן רישוי למתווכים</div>
                <div class="q-id">שאלה {st.session_state.current_q}</div>
            </div>
        """, unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"radio_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: 
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider()
            
            b_next, b_prev, b_finish = st.columns([1, 1, 1])
            with b_next:
                if st.session_state.current_q < 25:
                    if st.button("לשאלה הבאה", disabled=(choice is None), key="btn_next"):
                        logic.move_to_next()
                        st.rerun()
                else:
                    st.button("לשאלה הבאה", disabled=True, key="btn_next_off")

            with b_prev:
                if st.button("לשאלה הקודמת", disabled=(st.session_state.current_q == 1), key="btn_prev"):
                    st.session_state.current_q -= 1
                    st.rerun()
            
            with b_finish:
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="btn_finish_active")

# סוף קובץ
