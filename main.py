# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V125 | Date: 22/02/2026 | 23:59
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; box-sizing: border-box; }
    header, #MainMenu, footer { visibility: hidden; }
    
    .block-container { 
        max-width: 950px !important; 
        margin: 0 auto !important; 
        padding-top: 0rem !important; 
    }
    
    .header-box {
        border-bottom: 1px solid #eee;
        margin-top: 2px;
        margin-bottom: 5px;
    }

    .flex-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        padding: 5px 0;
    }

    /* שורת כותרת ושעון דחוסה למעלה */
    .exam-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0px;
        padding-top: 0px;
        margin-bottom: 10px;
    }

    @media (max-width: 768px) {
        .mobile-spacer { height: 50px; }
        .exam-header-row { flex-direction: column; gap: 0px; }
        h2 { font-size: 1.2rem !important; text-align: center !important; margin: 2px 0 !important; }
        .mobile-inst-padding { padding-right: 25px !important; }
    }

    /* עיצוב מספרים לניווט */
    .nav-num-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 12px;
        margin-top: 10px;
    }
    
    div[data-testid="stHorizontalBlock"] button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        color: #007bff !important;
        text-decoration: underline;
        font-size: 1rem !important;
        min-width: auto !important;
    }
    div[data-testid="stHorizontalBlock"] button:disabled {
        color: #000 !important;
        text-decoration: none !important;
        background: none !important;
    }

    .q-text { font-size: 1.2rem; font-weight: bold; line-height: 1.3; margin-bottom: 10px; }
    .stDivider { margin: 0.5rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="mobile-spacer"></div>', unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (עוגן V120)
st.markdown(f"""
    <div class="flex-header">
        <div style="text-align: left; flex: 1;">🏠 מתווך בקליק</div>
        <div style="text-align: center; color: #eee; flex: 0.2;">|</div>
        <div style="text-align: right; flex: 1;">👤 {user_name}</div>
    </div>
    <div class="header-box"></div>
""", unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center; margin-top:0;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    
    # מרכוז מדויק מעוגן V120
    _, center_col, _ = st.columns([0.1, 1.8, 0.1])
    with center_col:
        st.markdown('<div class="mobile-inst-padding">', unsafe_allow_html=True)
        instructions = [
            "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
            "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
            "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
        ]
        for i, txt in enumerate(instructions, 1):
            st.write(f"{i}. {txt}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        f_c1, f_c2 = st.columns([1, 1])
        with f_c1:
            agree = st.checkbox("קראתי את ההוראות")
        with f_c2:
            if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
                logic.start_exam_logic()
                st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    timer_html = f"""
    <div id="t-disp" style="font-weight: bold; font-family: monospace; color: #333; font-size: 1.1rem; text-align: center;"></div>
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

    # שורת כותרת ושעון צמודה למעלה
    st.markdown('<div class="exam-header-row">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin:0; padding:0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
    components.html(timer_html, height=30, width=100)
    st.markdown('</div>', unsafe_allow_html=True)

    q = st.session_state.exam_data.get(st.session_state.current_q)
    if q:
        st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom: 2px;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
        
        prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
        choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
        if choice is not None: 
            st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
        
        st.divider()
        
        # כפתורי ניווט מקוריים
        bn, bp, bf = st.columns(3)
        with bn:
            if st.session_state.current_q < 25:
                if st.button("לשאלה הבאה ⬅️", disabled=(choice is None)):
                    logic.move_to_next(); st.rerun()
        with bp:
            if st.button("➡️ לשאלה הקודמת", disabled=(st.session_state.current_q == 1)):
                st.session_state.current_q -= 1; st.rerun()
        with bf:
            if 25 in st.session_state.answers_user:
                st.button("סיום בחינה ✅", key="finish")

        # מפת מספרים תחתונה דחוסה
        st.markdown('<div class="nav-num-container">', unsafe_allow_html=True)
        num_cols = st.columns(25)
        for i in range(1, 26):
            with num_cols[i-1]:
                is_active = i in st.session_state.nav_active_questions
                if st.button(str(i), key=f"map_{i}", disabled=not is_active):
                    st.session_state.current_q = i; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# סוף קובץ
