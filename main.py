# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V73 | Date: 22/02/2026 | 23:45
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* הגדרות בסיס וביטול אלמנטים של Streamlit */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    
    /* מרווח עליון כדי למנוע חפיפה עם הסטריפ המערכתי */
    .block-container { 
        max-width: 1100px !important; 
        margin: 0 auto !important; 
        padding-top: 65px !important; 
    }
    
    /* Header - חזרה למבנה עמודות תקני */
    .header-style { 
        border-bottom: 2px solid #f0f0f0; 
        padding-bottom: 10px; 
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-right { font-size: 1.2rem; font-weight: bold; color: #333; }
    .header-left { font-size: 1rem; color: #666; }

    /* דף הוראות - ריווח ימני לנייד */
    .instruction-wrapper { 
        padding-right: 30px; 
        line-height: 1.6; 
        text-align: right;
    }

    /* התאמות לנייד */
    @media (max-width: 768px) {
        .block-container { padding-top: 55px !important; padding-right: 15px !important; padding-left: 15px !important; }
        .desktop-nav-content { display: none !important; }
        .header-right { font-size: 1rem !important; }
    }

    /* עיצוב מספרים במפה (במקום כפתורים) */
    .nav-number {
        display: inline-block;
        width: 35px;
        height: 35px;
        line-height: 35px;
        text-align: center;
        margin: 4px;
        border-radius: 5px;
        font-weight: bold;
        text-decoration: none;
    }
    .nav-active { color: #007bff; cursor: pointer; border: 1px solid #007bff; }
    .nav-inactive { color: #ccc; cursor: default; border: 1px solid #eee; }
    .nav-current { background-color: #007bff; color: white !important; }

    .q-text { font-size: 1.25rem; font-weight: bold; margin-bottom: 10px; }
    .stDivider { margin: 0.5rem 0 !important; }
    </style>
""", unsafe_allow_html=True)

# Header - מבנה עוגן
st.markdown(f"""
    <div class="header-style">
        <div class="header-right">🏠 מתווך בקליק</div>
        <div class="header-left">👤 משתמש: {user_name}</div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    with center_col:
        st.markdown('<h2 style="text-align: center;">הוראות למבחן</h2>', unsafe_allow_html=True)
        st.markdown('<div class="instruction-wrapper">', unsafe_allow_html=True)
        instructions = ["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", "ניתן לחזור אחורה רק לשאלות שנענו.", "ציון עובר: 60.", "אין להשתמש בחומר עזר."]
        for i, txt in enumerate(instructions, 1): st.write(f"{i}. {txt}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        agree = st.checkbox("קראתי והבנתי את ההוראות")
        if st.button("התחל בחינה", disabled=not (agree and logic.is_first_question_ready())):
            logic.start_exam_logic()
            st.rerun()

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    def get_timer_html(font_size):
        return f"""
        <div id="timer-display" style="text-align: center; border: 2px solid #333; padding: 5px; border-radius: 8px; font-weight: bold; font-size: {font_size}; font-family: monospace;"></div>
        <script>
        var seconds = {rem_sec};
        function update() {{
            var m = Math.floor(seconds / 60);
            var s = seconds % 60;
            var el = document.getElementById('timer-display');
            if (el) {{
                el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
                if (seconds <= 600) el.style.color = "red";
            }}
            if (seconds > 0) seconds--;
        }}
        update(); setInterval(update, 1000);
        </script>
        """

    col_nav, col_main = st.columns([1, 3], gap="medium")
    
    with col_nav:
        components.html(get_timer_html("1.3rem"), height=50)
        st.markdown('<div class="desktop-nav-content">', unsafe_allow_html=True)
        st.write("**מפת שאלות:**")
        
        # תצוגת מספרים לפי הפרוטוקול
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    is_answered = idx in st.session_state.nav_active_questions
                    is_current = (idx == st.session_state.current_q)
                    
                    if is_current:
                        cols[i].markdown(f'<div class="nav-number nav-current">{idx}</div>', unsafe_allow_html=True)
                    elif is_answered:
                        if cols[i].button(str(idx), key=f"btn_{idx}"):
                            st.session_state.current_q = idx
                            st.rerun()
                    else:
                        cols[i].markdown(f'<div class="nav-number nav-inactive">{idx}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f'<p style="color: #666; margin-bottom:0;">שאלה {st.session_state.current_q} מתוך 25</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="q-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            current_ans = st.session_state.answers_user.get(st.session_state.current_q)
            choice = st.radio("בחר תשובה:", q["options"], index=current_ans, key=f"q_{st.session_state.current_q}", label_visibility="collapsed")
            
            if choice is not None:
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(choice)
            
            st.divider()
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("הבא ➔", disabled=(choice is None), use_container_width=True):
                    logic.move_to_next()
                    st.rerun()
            with c2:
                if st.button("⬅ הקודם", disabled=(st.session_state.current_q == 1), use_container_width=True):
                    st.session_state.current_q -= 1
                    st.rerun()
            with c3:
                if len(st.session_state.answers_user) >= 25:
                    st.button("סיום מבחן", type="primary", use_container_width=True)

# סוף קובץ
