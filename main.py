# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Claude 03 | Fix desktop header, mobile header visibility, spacing
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- SECTION: GENERAL --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 8px; }

    /* --- SECTION: DESKTOP --- */
    @media (min-width: 769px) {
        .nav-title { display: block; margin-bottom: 10px; font-weight: bold; }
        .question-area { padding-right: 8%; padding-left: 8%; }
        .mobile-header { display: none !important; }
    }

    /* --- SECTION: MOBILE --- */
    @media (max-width: 768px) {
        .block-container { padding-top: 60px !important; }
        .mobile-up { margin-top: 0px !important; }
        .nav-title { margin-top: 10px !important; text-align: center; display: block; }
        iframe { width: 100% !important; height: 50px !important; }
        .desktop-header { display: none !important; }
        .mobile-header {
            display: flex !important;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 0;
            width: fit-content;
            margin: 4px auto 4px auto;
            font-size: 1.1rem;
            font-weight: bold;
        }
        .mobile-header-spacer {
            display: inline-block;
            width: 3em;
        }
    }
    </style>
""", unsafe_allow_html=True)

# אתחול
logic.initialize_exam_state()

# סטריפ עליון — מחשב
st.markdown(f"""
    <div class="desktop-header">
        <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:5px; border-bottom:1px solid #eee; margin-bottom:15px;">
            <div style="font-weight:bold; font-size:1.1rem;">🏠 מתווך בקליק</div>
            <div style="font-weight:bold;">👤 {user_name}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# סטריפ עליון — נייד
st.markdown(f"""
    <div class="mobile-header">
        <div style="white-space:nowrap;">🏠 מתווך בקליק</div>
        <div class="mobile-header-spacer"></div>
        <div style="white-space:nowrap;">👤 {user_name}</div>
    </div>
""", unsafe_allow_html=True)

current_step = st.session_state.get("step", "instructions")

if current_step == "instructions":
    logic.ensure_question_exists(1)
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מתווכים</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה לשאלות שנחשפו.", "ציון עובר: 60."]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.write("")
        f_cols = st.columns([1, 1])
        with f_cols[0]: agree = st.checkbox("קראתי את ההוראות")
        with f_cols[1]:
            if st.button("התחל בחינה", disabled=not (agree and 1 in st.session_state.exam_data)):
                st.session_state.step = "exam_run"; st.session_state.current_q = 1
                st.session_state.nav_active_questions.add(1); logic.ensure_question_exists(2); st.rerun()

elif current_step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    header_html = f"""
    <style>
        .wrapper {{
            direction: rtl; display: flex; align-items: center; justify-content: center; width: 100%;
            margin-top: 4px; margin-bottom: 4px;
        }}
        .t-text {{ font-size: 2.2rem; font-weight: bold; color: #000; white-space: nowrap; }}
        .c-text {{ font-size: 2rem; font-weight: bold; margin-right: 30px; direction: ltr; }}

        @media (max-width: 768px) {{
            .wrapper {{ justify-content: center !important; gap: 15px !important; margin-top: 2px !important; margin-bottom: 2px !important; }}
            .t-text {{ font-size: 1rem !important; }}
            .c-text {{ font-size: 1rem !important; margin-right: 0 !important; }}
        }}
    </style>
    <div class="wrapper">
        <div class="t-text">מבחן רישוי למתווכים</div>
        <div id="clock-val" class="c-text"></div>
    </div>
    <script>
    var s = {rem_sec};
    function u() {{
        var m = Math.floor(s / 60); var sec = s % 60;
        var el = document.getElementById('clock-val');
        if (el) {{
            el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
            if (s <= 600) el.style.color = "red";
        }}
        if (s > 0) s--;
    }}
    u(); setInterval(u, 1000);
    </script>
    """
    components.html(header_html, height=50)

    col_main, col_nav = st.columns([2.5, 1], gap="medium")
    with col_main:
        st.markdown('<div class="question-area" style="margin-top:8px;">', unsafe_allow_html=True)
        idx = st.session_state.current_q
        q = st.session_state.exam_data.get(idx)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom: 2px;">שאלה {idx}</p>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:1.2rem; font-weight:bold; margin-bottom:15px;">{q["question"]}</div>', unsafe_allow_html=True)
            choice = st.radio("", q["options"], index=st.session_state.answers_user.get(idx), key=f"r_{idx}", label_visibility="collapsed")
            if choice is not None:
                st.session_state.answers_user[idx] = q["options"].index(choice)
                if idx == 25: st.session_state.finish_button_visible = True
            st.divider()
            b_p, b_n, b_f = st.columns([1, 1, 1.2])
            with b_p:
                if idx > 1 and st.button("לשאלה הקודמת"): st.session_state.current_q -= 1; st.rerun()
            with b_n:
                if idx < 25:
                    if st.button("לשאלה הבאה", disabled=not (idx in st.session_state.answers_user and (idx+1) in st.session_state.exam_data)):
                        st.session_state.current_q += 1; st.session_state.nav_active_questions.add(st.session_state.current_q)
                        if idx <= 23: logic.ensure_question_exists(idx + 2)
                        st.rerun()
            with b_f:
                if st.session_state.get("finish_button_visible") and st.button("סיים בחינה", type="primary"):
                    st.session_state.step = "feedback"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_nav:
        st.markdown('<div class="nav-title">מפת שאלות:</div>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                n = r + i + 1
                if n <= 25:
                    is_active = n in st.session_state.nav_active_questions
                    if cols[i].button(f"**{n}**" if n == st.session_state.current_q else str(n), key=f"n_{n}", disabled=not is_active):
                        st.session_state.current_q = n; st.rerun()
# סוף קובץ
