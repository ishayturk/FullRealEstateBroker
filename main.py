# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V123 | Date: 22/02/2026 | 23:55
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
        max-width: 900px !important; 
        margin: 0 auto !important; 
        padding-top: 0.5rem !important; 
    }
    
    .header-box {
        border-bottom: 1px solid #eee;
        margin-top: 5px;
        margin-bottom: 15px;
    }

    .flex-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        padding: 5px 0;
        gap: 10px;
    }
    .flex-header div {
        white-space: nowrap;
        font-weight: bold;
        font-size: 1.1rem;
    }

    @media (max-width: 768px) {
        .mobile-spacer { height: 50px; }
        h2 { font-size: 1.3rem !important; text-align: center !important; }
        .flex-header div { font-size: 1rem; }
    }

    /* עיצוב שעון מרכזי */
    .timer-wrapper {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }

    /* עיצוב מפת שאלות תחתונה */
    .nav-map-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-top: 20px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
    }

    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 15px; color: #000; text-align: center; }
    .stDivider { margin: 1rem 0 !important; }
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
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    
    # מרכז העמוד במבנה Stack
    st.markdown('<div style="max-width: 600px; margin: 0 auto;">', unsafe_allow_html=True)
    instructions = [
        "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", 
        "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", 
        "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
    ]
    for i, txt in enumerate(instructions, 1):
        st.write(f"{i}. {txt}")
    
    st.write("")
    f_c1, f_c2 = st.columns([1, 1])
    with f_c1:
        agree = st.checkbox("קראתי את ההוראות")
    with f_c2:
        if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
            logic.start_exam_logic()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    # שעון מרכזי אחד לשני המצבים (מותאם ב-HTML)
    timer_html = f"""
    <div id="t-disp" style="text-align: center; font-weight: bold; font-family: monospace; color: #333; font-size: 1.5rem; padding: 5px;"></div>
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
    
    st.markdown('<div class="timer-wrapper">', unsafe_allow_html=True)
    components.html(timer_html, height=50)
    st.markdown('</div>', unsafe_allow_html=True)

    # אזור השאלה - תופס את כל הרוחב
    st.markdown('<h2 style="text-align: center; margin-top: 0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
    
    q = st.session_state.exam_data.get(st.session_state.current_q)
    if q:
        st.markdown(f'<p style="text-align: center; color: #888; font-weight: bold;">שאלה {st.session_state.current_q} מתוך 25</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
        
        # מרכוז רדיו בתוך בלוק
        _, r_col, _ = st.columns([0.1, 0.8, 0.1])
        with r_col:
            prev_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("", q["options"], index=prev_ans, key=f"r_{st.session_state.current_q}", label_visibility="collapsed")
            if choice is not None: 
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
        
        st.divider()
        
        # כפתורי ניווט
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

        # מפת שאלות תחתונה (שורת מספרים)
        st.markdown('<div class="nav-map-container">', unsafe_allow_html=True)
        # שימוש בעמודות Streamlit ליצירת שורת כפתורים אופקית
        map_cols = st.columns(13) # שורה ראשונה
        for i in range(1, 14):
            with map_cols[i-1]:
                is_active = i in st.session_state.nav_active_questions
                is_curr = i == st.session_state.current_q
                label = f"[{i}]" if is_curr else str(i)
                if st.button(label, key=f"map_{i}", disabled=not is_active, use_container_width=True):
                    st.session_state.current_q = i; st.rerun()
        
        map_cols2 = st.columns(12) # שורה שנייה
        for i in range(14, 26):
            with map_cols2[i-14]:
                is_active = i in st.session_state.nav_active_questions
                is_curr = i == st.session_state.current_q
                label = f"[{i}]" if is_curr else str(i)
                if st.button(label, key=f"map_{i}", disabled=not is_active, use_container_width=True):
                    st.session_state.current_q = i; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# סוף קובץ
