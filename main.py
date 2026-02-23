# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V131 | Date: 23/02/2026 | 09:15
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- 1. מגזר כללי (Shared) --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    
    .block-container { 
        max-width: 1100px !important; 
        margin: 0 auto !important; 
        padding-top: 0.5rem !important; 
    }
    
    .header-box {
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    .q-text { font-size: 1.25rem; font-weight: bold; line-height: 1.4; margin-bottom: 10px; color: #000; }
    .stDivider { margin: 0.5rem 0 !important; }

    /* --- 2. מגזר מחשב (Desktop Only) --- */
    @media (min-width: 769px) {
        div[data-testid="column"]:nth-of-type(1) {
            background-color: #f1f3f5 !important;
            border-radius: 15px;
            padding: 15px !important;
        }
        .nav-title { margin-top: -10px !important; margin-bottom: 5px !important; display: block; }
        
        #timer-display {
            text-align: center; 
            background: #ffffff; 
            border: 3px solid #000; 
            padding: 12px; 
            border-radius: 10px; 
            font-weight: 900; 
            font-size: 1.8rem; 
            color: #000; 
            font-family: monospace;
        }
    }

    /* --- 3. מגזר נייד (Mobile Only) --- */
    @media (max-width: 768px) {
        #timer-display {
            text-align: left;
            font-size: 1.4rem;
            font-weight: bold;
            color: #333;
            padding-bottom: 10px;
        }
        .q-text { margin-top: 15px; }
    }
    </style>
""", unsafe_allow_html=True)

logic.initialize_exam()

# 1. סטריפ עליון (V113)
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)

st.markdown('<div class="header-box"></div>', unsafe_allow_html=True)

# 2. תוכן
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h2>', unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
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

elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    timer_html = f"""
    <div id="timer-display"></div>
    <script>
    var s = {rem_sec};
    function u() {{
        var m = Math.floor(s / 60); var sec = s % 60;
        var el = document.getElementById('timer-display');
        if (el) {{
            if (s <= 600) el.style.color = "red";
            el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
        }}
        if (s > 0) s--;
    }}
    u(); setInterval(u, 1000);
    </script>
    """

    # בדיקת רוחב מסך פשוטה דרך JS להחלטה על המבנה (בתוספת ל-CSS)
    # ב-Streamlit הדרך הכי עניינית להפריד עמודות היא פשוט לבנות אותן אחרת
    
    # שימוש ב-st.columns רק אם לא "נייד" (לפי לוגיקה פשוטה של Streamlit)
    # הערה: Streamlit לא יודע בזמן אמת על רוחב הדפדפן בפייתון, 
    # לכן נשתמש במבנה עמודות שמתפרק בנייד, אך ננקה את תוכן עמודת הניווט בנייד דרך ה-CSS שכתבנו למעלה.
    
    col_nav, col_main = st.columns([1, 2.5], gap="medium")
    
    with col_nav:
        # הקוד הזה ירוץ, אך ה-CSS יעלים את כל העמודה הזו בנייד (display: none)
        components.html(timer_html, height=80)
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

    with col_main:
        # בנייד, נזריק שעון נוסף שיופיע רק שם (ה-
