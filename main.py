# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V211 | Date: 24/02/2026 | 01:00
import streamlit as st
import logic
import streamlit.components.v1 as components

# הגדרות עמוד
st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

# עיצוב CSS (כללי, דסקטופ, מובייל)
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

# אתחול משתנים
logic.initialize_exam_state()

# סטריפ עליון (Logo, Name, Divider)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)
st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# ניהול שלבים
current_step = st.session_state.get("step", "instructions")

if current_step == "instructions":
    # הכנת שאלה 1 בברקע
    logic.ensure_question_exists(1)
    
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        instructions = [
            "המבחן כולל 25 שאלות.",
            "זמן מוקצב: 90 דקות.",
            "מעבר לשאלה הבאה דורש סימון תשובה והמתנה לטעינה.",
            "ניתן לחזור אחורה לשאלות שכבר נחשפו.",
            "ציון עובר: 60."
        ]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        
        st.write("")
        agree = st.checkbox("קראתי והבנתי את ההוראות")
        
        # תנאי כפול: צ'קבוקס + שאלה 1 מוכנה ב-Buffer
        is_q1_ready = 1 in st.session_state.exam_data
        
        if st.button("התחל בחינה", disabled=not (agree and is_q1_ready)):
            st.session_state.step = "exam_run"
            st.session_state.current_q = 1
            st.session_state.nav_active_questions.add(1)
            # ייצור שאלה 2 מיד עם הכניסה
            logic.ensure_question_exists(2)
            st.rerun()
            
        if agree and not is_q1_ready:
            st.caption("מכין את הבחינה... מיד נתחיל.")

elif current_step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    # טיימר עליון
    components.html(f"""
    <div style="direction: rtl; display: flex; align-items: center; justify-content: center; width: 100%;">
        <div style="font-size: 2.2rem; font-weight: bold; color: #000;">מבחן רישוי למתווכים</div>
        <div id="clock-val" style="font-size: 2rem; font-weight: bold; margin-right: 30px; direction: ltr;"></div>
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
    """, height=70)

    col_main, col_nav = st.columns([2.5, 1], gap="medium")
    
    with col_main:
        st.markdown('<div class="mobile-up">', unsafe_allow_html=True)
        curr_q_idx = st.session_state.current_q
        q = st.session_state.exam_data.get(curr_q_idx)
        
        if q:
            st.markdown(f'<p style="color: #888; font-weight: bold; margin-bottom: 2px;">שאלה {curr_q_idx}</p>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:1.2rem; font-weight:bold; margin-bottom:15px;">{q["question"]}</div>', unsafe_allow_html=True)
            
            prev_ans = st.session_state.answers_user.get(curr_q_idx)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{curr_q_idx}", label_visibility="collapsed")
            
            if choice is not None:
                st.session_state.answers_user[curr_q_idx] = q["options"].index(choice)
                if curr_q_idx == 25:
                    st.session_state.finish_button_visible = True
            
            st.divider()
            
            b_prev, b_next, b_finish = st.columns([1, 1, 1.2])
            with b_prev:
                if curr_q_idx > 1:
                    if st.button("לשאלה הקודמת"):
                        st.session_state.current_q -= 1
                        st.rerun()
            
            with b_next:
                if curr_q_idx < 25:
                    is_answered = curr_q_idx in st.session_state.answers_user
                    is_next_ready = (curr_q_idx + 1) in st.session_state.exam_data
                    # חסימת מעבר אם השאלה הבאה עוד לא נוצרה ב-Buffer
                    if st.button("לשאלה הבאה", disabled=not (is_answered and is_next_ready)):
                        st.session_state.current_q += 1
                        st.session_state.nav_active_questions.add(st.session_state.current_q)
                        # ייצור X+2 רק אם צריך
                        if curr_q_idx <= 23:
                            logic.ensure_question_exists(curr_q_idx + 2)
                        st.rerun()
                else:
                    st.button("לשאלה הבאה", disabled=True)

            with b_finish:
                if st.session_state.finish_button_visible:
                    if st.button("סיים בחינה", type="primary"):
                        st.session_state.step = "feedback"
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_nav:
        st.markdown('<div class="nav-title">מפת שאלות:</div>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.nav_active_questions
                    label = f"**{idx}**" if idx == st.session_state.current_q else str(idx)
                    if cols[i].button(label, key=f"n_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx
                        st.rerun()

# סוף קובץ
