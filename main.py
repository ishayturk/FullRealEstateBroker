# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V28 | Date: 22/02/2026 | 00:50
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    
    .main-wrapper {
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 10px;
    }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 0; border-bottom: 1px solid #eee;
        margin-bottom: 30px; position: relative; z-index: 1000;
    }
    
    .nav-panel { background-color: #f8f9fa; border: 1px solid #e1e4e8; padding: 20px; border-radius: 12px; }
    
    .timer-display {
        text-align: center; background: #fff; border: 2px solid #333;
        padding: 10px; border-radius: 8px; font-weight: bold;
        font-size: 1.6rem; color: #333; margin-bottom: 20px; font-family: monospace;
    }

    .centered-box { max-width: 700px; margin: 0 auto; }
    .exam-title-main { font-size: 1.8rem; font-weight: bold; text-align: center; margin-top: 10px; }
    .exam-subtitle { font-size: 1.1rem; color: #555; text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# תחילת המעטפת הממורכזת
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# סטריפ עליון - תופס רק את רוחב המעטפת
st.markdown(f"""
    <div class="fixed-header">
        <div style="font-size: 1.3rem;">🏠 <b>מתווך בקליק</b></div>
        <div style="font-size: 1.2rem;">👤 <b>{user_name}</b></div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<div class="centered-box">', unsafe_allow_html=True)
    st.title("הוראות למבחן רישויי מקרקעין")
    instructions = [
        "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.",
        "ניתן לחזור אחורה רק לשאלות שנענו.", "בסיום 90 דקות המבחן יינעל.",
        "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
    ]
    for i, txt in enumerate(instructions, 1):
        st.write(f"{i}. {txt}")
    
    st.write("")
    c1, c2 = st.columns([1.5, 1])
    with c1: agree = st.checkbox("קראתי את ההוראות")
    with c2:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        st.markdown('<div class="nav-panel">', unsafe_allow_html=True)
        rem = logic.get_remaining_seconds()
        # השעון מוזרק עם ערך הזמן הנוכחי מפייתון
        st.markdown(f"""
            <div class="timer-display" id="js-timer">--:--</div>
            <script>
            (function() {{
                var timeLeft = {rem};
                var el = document.getElementById('js-timer');
                function update() {{
                    var m = Math.floor(timeLeft / 60);
                    var s = timeLeft % 60;
                    el.innerHTML = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
                    if (timeLeft > 0) timeLeft--;
                }}
                update();
                setInterval(update, 1000);
            }})();
            </script>
        """, unsafe_allow_html=True)
        
        st.write("<b>ניווט:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    if idx <= st.session_state.max_reached:
                        if cols[i].button(str(idx), key=f"n_{idx}"):
                            st.session_state.current_q = idx; st.rerun()
                    else:
                        cols[i].markdown(f"<div style='color:#ccc; text-align:center;'>{idx}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div class="exam-title-main">מבחן רישוי למתווכים</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exam-subtitle">שאלה {st.session_state.current_q} מתוך 25</div>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f"#### {q['question']}")
            ans = st.radio("בחר תשובה:", q["options"], 
                           index=st.session_state.answers_user.get(st.session_state.current_q),
                           key=f"r_{st.session_state.current_q}")
            if ans: 
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(ans)
            
            st.divider()
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("הקודם", disabled=(st.session_state.current_q==1)):
                    logic.handle_navigation("prev"); st.rerun()
            with b2:
                can = (st.session_state.current_q in st.session_state.answers_user and st.session_state.current_q < 25)
                if st.button("הבא", disabled=not can):
                    logic.handle_navigation("next"); st.rerun()
            with b3:
                if 25 in st.session_state.answers_user:
                    if st.button("סיום"): st.session_state.step = "summary"; st.rerun()

st.markdown('</div>', unsafe_allow_html=True) # סגירת wrapper

# סוף קובץ
