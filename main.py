# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V127 | Date: 23/02/2026 | 00:40
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
    
    .header-box { border-bottom: 1px solid #eee; margin-bottom: 15px; }

    .flex-header {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; padding: 5px 0;
    }

    /* סידור כותרת ושעון - דחיסה למעלה עם מרווח בטיחות מהשאלה */
    .title-timer-container {
        display: flex; justify-content: space-between; align-items: center;
        width: 100%; margin-bottom: 30px; /* מרווח למניעת חפיפה עם השאלה */
    }
    .title-timer-container h2 { margin: 0 !important; font-size: 1.5rem !important; }

    @media (max-width: 768px) {
        .mobile-spacer { height: 50px; }
        .title-timer-container { flex-direction: column; gap: 10px; text-align: center; }
        .title-timer-container h2 { font-size: 1.2rem !important; }
    }

    /* עיצוב השאלה - צמצום רווחים פנימיים */
    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 15px; color: #000; }
    div[data-testid="stRadio"] { margin-bottom: -10px !important; }
    
    /* מפת מספרים - טקסט נקי מתחת לקו */
    .nav-num-map {
        display: flex; flex-wrap: wrap; justify-content: center;
        gap: 12px; margin-top: 20px; padding-bottom: 20px;
    }
    
    /* הפיכת כפתורי המפה לטקסט לחיץ בלבד */
    div[data-testid="column"] button[key^="map_"] {
        background: none !important; border: none !important; padding: 0 !important;
        color: #007bff !important; text-decoration: underline;
        font-size: 1.1rem !important; min-width: auto !important;
    }
    div[data-testid="column"] button[key^="map_"]:disabled {
        color: #333 !important; text-decoration: none !important; cursor: default !important;
    }

    /* מרכוז דף הסבר - שחזור V67 */
    .instructions-wrapper {
        max-width: 750px; margin: 0 auto; text-align: right; padding: 10px;
    }
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
    st.markdown('<div class="instructions-wrapper">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    
    # שחזור תוכן מלא מגרסה 67
    st.write("1. המבחן כולל 25 שאלות רב-ברירתיות (אמריקאיות).")
    st.write("2. הזמן המוקצב למבחן הוא 90 דקות.")
    st.write("3. ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה לשאלות קודמות שנענו לצורך בדיקה או שינוי.")
    st.write("5. ציון המעבר בבחינה הוא 60.")
    st.write("6. חל איסור מוחלט על שימוש בחומר עזר או בטלפונים ניידים.")
    
    st.write("")
    f_c1, f_c2 = st.columns([1, 1])
    with f_c1:
        agree = st.checkbox("קראתי את ההוראות ואני מוכן/ה להתחיל")
    with f_c2:
        if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
            logic.start_exam_logic()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    timer_js = f"""
    <div id="t-disp" style="font-weight: bold; font-family: monospace; color: #333; font-size: 1.3rem; text-align: left;"></div>
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

    # שורת כותרת ושעון (במחשב שורה אחת, בנייד שתיים)
    st.markdown('<div class="title-timer-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin:0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
    components.html(timer_js, height=35, width=120)
    st.markdown('</div>', unsafe_allow_html=True)

    q = st.session_state.exam_data.get(st.session_state.current_q)
    if q:
        st.markdown(f'<p style="color: #888; font-weight: bold; margin: 0;">שאלה {st.session_state.current_q} מתוך 25</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
        
        prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
        choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
        if choice is not None: 
            st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
        
        # כפתורי ניווט (הבא/קודם) - עיצוב כפתורים מלאים
        st.write("")
        bn, bp, bf = st.columns(3)
        with bn:
            if st.session_state.current_q < 25:
                if st.button("לשאלה הבאה ⬅️", disabled=(choice is None), use_container_width=True):
                    logic.move_to_next(); st.rerun()
        with bp:
            if st.button("➡️ לשאלה הקודמת", disabled=(st.session_state.current_q == 1), use_container_width=True):
                st.session_state.current_q -= 1; st.rerun()
        with bf:
            if 25 in st.session_state.answers_user:
                st.button("סיום בחינה ✅", key="finish", use_container_width=True)

        # קו מפריד בין הכפתורים למפת המספרים
        st.divider()

        # מפת מספרים (טקסט לחיץ בלבד)
        st.markdown('<div class="nav-num-map">', unsafe_allow_html=True)
        num_cols = st.columns(25)
        for i in range(1, 26):
            with num_cols[i-1]:
                is_active = i in st.session_state.nav_active_questions
                if st.button(str(i), key=f"map_{i}", disabled=not is_active):
                    st.session_state.current_q = i; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# סוף קובץ
