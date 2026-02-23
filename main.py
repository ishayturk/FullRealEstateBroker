# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V133 | Date: 23/02/2026 | 09:45
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- 1. כללי --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 15px; }
    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }

    /* --- 2. מחשב (Desktop) --- */
    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 15px !important;
        }
        .desktop-only { display: block; }
        .mobile-only { display: none; }
    }

    /* --- 3. נייד (Mobile) --- */
    @media (max-width: 768px) {
        /* ביטול מוחלט של פריים הניווט */
        div[data-testid="column"]:nth-of-type(1) {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }
        /* הרחבת הפריים המרכזי לכל הרוחב */
        div[data-testid="column"]:nth-of-type(2) {
            width: 100% !important;
            min-width: 100% !important;
        }
        .desktop-only { display: none; }
        .mobile-only { display: block; }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (V113)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: 
    if st.button("🏠 מתווך בקליק", key="back_btn"):
        st.session_state.step = "instructions"
        st.rerun()
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.write("")
        agree = st.checkbox("קראתי את ההוראות")
        if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
            logic.start_exam_logic()
            st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    # פונקציית עזר ליצירת שעון
    def render_timer(is_mobile=False):
        style = "font-size: 1.2rem; font-weight: bold; text-align: left;" if is_mobile else "font-size: 1.8rem; font-weight: 900; text-align: center; background: #fff; border: 2px solid #000; padding: 10px; border-radius: 8px;"
        return f"""
        <div id="timer-val" style="{style}"></div>
        <script>
        var s = {rem_sec};
        function u() {{
            var m = Math.floor(s / 60); var sec = s % 60;
            var el = document.getElementById('timer-val');
            if (el) {{
                if (s <= 600) el.style.color = "red";
                el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
            }}
            if (s > 0) s--;
        }}
        u(); setInterval(u, 1000);
        </script>
        """

    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        # פריים ניווט (מוסתר בנייד דרך CSS)
        st.markdown('<div class="desktop-only">', unsafe_allow_html=True)
        components.html(render_timer(False), height=100)
        st.markdown('<b class="nav-title">מפת שאלות:</b>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.nav_active_questions
                    label = f"**{idx}**" if idx == st.session_state.current_q else str(idx)
                    if cols[i].button(label, key=f"n_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        # שעון לנייד בלבד
        st.markdown('<div class="mobile-only">', unsafe_allow_html=True)
        components.html(render_timer(True), height=50)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<h2 style="text-align: center; margin-top: 0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold;">שאלה {st.session_state.current_q}</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: 
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider()
            
            bn, bp, bf = st.columns(3)
            with bn:
                if st.session_state.current_q < 25:
                    if st.button("לשאלה הבאה", disabled=(choice is None), key="next"):
                        logic.move_to_next(); st.rerun()
            with bp:
                if st.button("לשאלה הקודמת", disabled=(st.session_state.current_q == 1), key="prev"):
                    st.session_state.current_q -= 1; st.rerun()
            with bf:
                if 25 in st.session_state.answers_user:
                    st.button("סיום בחינה", key="finish")

# סוף קובץ
