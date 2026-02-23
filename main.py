# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V213 | Date: 24/02/2026 | 01:30
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
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 15px; }
    
    /* --- SECTION: DESKTOP --- */
    @media (min-width: 769px) {
        .nav-title { display: block; margin-bottom: 10px; font-weight: bold; }
    }

    /* --- SECTION: MOBILE --- */
    @media (max-width: 768px) {
        .block-container { padding-top: 0px !important; }
        .mobile-up { margin-top: -90px !important; }
        .nav-title { margin-top: 25px !important; text-align: center; display: block; }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam_state()

# סטריפ עליון - עוגן V38
st.write("")
h_col1, h_col2, h_col3 = st.columns([1, 2, 1])
with h_col3: st.markdown('<div style="text-align: right; font-weight: bold;">מתווך בקליק</div>', unsafe_allow_html=True)
with h_col2: st.markdown(f'<div style="text-align: center; font-weight: bold;">{user_name}</div>', unsafe_allow_html=True)
with h_col1: 
    if st.button("חזרה", key="back_home"): pass

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

step = st.session_state.get("step", "instructions")

if step == "instructions":
    logic.ensure_question_exists(1)
    # עמוד הסבר - עוגן V38
    st.markdown('<h1 style="text-align: center;">מבחן רשם המתווכים</h1>', unsafe_allow_html=True)
    st.write("ברוכים הבאים למערכת סימולציית הבחינה של רשם המתווכים.")
    st.write("המבחן מדמה את התנאים האמיתיים של הבחינה הממשלתית.")
    st.markdown("### דגשים חשובים:")
    st.write("* המבחן כולל 25 שאלות רב-ברירה.")
    st.write("* משך הבחינה המומלץ הוא 90 דקות.")
    st.write("* לכל שאלה תשובה אחת נכונה בלבד.")
    st.write("")
    
    agree = st.checkbox("אני מאשר כי קראתי את ההוראות")
    is_q1_ready = 1 in st.session_state.exam_data
    
    if st.button("עבור לבחינה", disabled=not (agree and is_q1_ready)):
        st.session_state.step = "exam_run"
        st.session_state.current_q = 1
        st.session_state.nav_active_questions.add(1)
        logic.ensure_question_exists(2)
        st.rerun()

elif step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    components.html(f'<div style="direction: rtl; display: flex; align-items: center; justify-content: center; width: 100%;"><div style="font-size: 2.2rem; font-weight: bold; color: #000;">מבחן רישוי למתווכים</div><div id="clock-val" style="font-size: 2rem; font-weight: bold; margin-right: 30px; direction: ltr;"></div></div><script>var s={rem_sec};function u(){{var m=Math.floor(s/60);var sec=s%60;var el=document.getElementById("clock-val");if(el){{el.innerHTML=(m<10?"0":"")+m+":"+(sec<10?"0":"")+sec;if(s<=600)el.style.color="red"}}if(s>0)s--}}u();setInterval(u,1000)</script>', height=70)

    col_main, col_nav = st.columns([2.5, 1], gap="medium")
    with col_main:
        st.markdown('<div class="mobile-up">', unsafe_allow_html=True)
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
            b_prev, b_next, b_finish = st.columns([1, 1, 1.2])
            with b_prev:
                if idx > 1:
                    if st.button("לשאלה הקודמת"):
                        st.session_state.current_q -= 1
                        st.rerun()
            with b_next:
                if idx < 25:
                    is_ready = (idx + 1) in st.session_state.exam_data
                    if st.button("לשאלה הבאה", disabled=not (idx in st.session_state.answers_user and is_ready)):
                        st.session_state.current_q += 1
                        st.session_state.nav_active_questions.add(st.session_state.current_q)
                        if idx <= 23: logic.ensure_question_exists(idx + 2)
                        st.rerun()
            with b_finish:
                if st.session_state.finish_button_visible and st.button("סיים בחינה", type="primary"):
                    st.session_state.step = "feedback"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_nav:
        st.markdown('<div class="nav-title">מפת שאלות:</div>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                n = r + i + 1
                if n <= 25:
                    label = f"**{n}**" if n == st.session_state.current_q else str(n)
                    if cols[i].button(label, key=f"n_{n}", disabled=n not in st.session_state.nav_active_questions):
                        st.session_state.current_q = n; st.rerun()
# סוף קובץ
