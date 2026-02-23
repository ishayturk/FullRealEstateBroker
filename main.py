# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V243 | Date: 23/02/2026 | 23:58
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
        
        /* תיקון רוחב וכיווץ כותרת ושעון */
        iframe { width: 100% !important; height: 50px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# אתחול
logic.initialize_exam_state()

# 1. סטריפ עליון (V208)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)
st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. ניהול שלבי הבחינה
current_step = st.session_state.get("step", "instructions")

if current_step == "instructions":
    logic.ensure_question_exists(1)
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מתווכים</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה לשאלות שנחשפו.", "ציון עובר: 60.", "המקור: חוק המתווכים, תקנות האתיקה ודיני המקרקעין."]
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
    # שימוש ב-Media Query פנימי בתוך ה-HTML כדי להבטיח התאמה מושלמת
    header_html = f"""
    <style>
        .wrapper {{
            direction: rtl; display: flex; align-items: center; justify-content: center; width: 100%; 
        }}
        .t-text {{ font-size: 2.2rem; font-weight: bold; color: #000; white-space: nowrap; }}
        .c-text {{ font-size: 2rem; font-weight: bold; margin-right: 30px; direction: ltr; }}
        
        @media (max-width: 768px) {{
            .wrapper {{ justify-content: space-between !important; padding: 0 5px; }}
            .t-text {{ font-size: 1.1rem !important; }}
            .c-text {{ font-size: 1.1rem !important; margin-right: 10px !important; }}
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
    components.html(header_html, height=60)

    col_main, col_nav = st.columns([2.5, 1], gap="medium")
    with col_main:
        st.markdown('<div class="mobile-up">', unsafe_allow_html=True)
        idx = st.session_state.current_q
        q = st.session_state.exam_data.get(idx)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom:
