# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V22 | Date: 22/02/2026 | 00:08
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", 
                   initial_sidebar_state="collapsed")

user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    [data-testid="stSidebar"] { display: none !important; }
    
    .block-container { max-width: 950px !important; margin: auto !important; padding-top: 1rem !important; }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #eee; margin-bottom: 30px;
    }
    
    .nav-panel {
        background-color: #f4f4f4; border: 1px solid #ddd; padding: 15px;
        border-radius: 10px; margin-left: 20px;
    }
    
    .timer-display {
        text-align: center; background: #fff; border: 1px solid #ccc;
        padding: 8px; border-radius: 5px; font-weight: bold;
        font-size: 1.4rem; color: #d32f2f; margin-bottom: 15px;
    }

    .centered-box { max-width: 750px; margin: 50px auto; text-align: center; }
    
    .exam-header-title {
        font-size: 1.5rem; font-weight: bold; color: #2c3e50;
        text-align: center; width: 100%; margin-bottom: 20px;
        border-bottom: 2px solid #3498db; padding-bottom: 10px;
    }

    @media (max-width: 600px) {
        .fixed-header { flex-direction: column; align-items: center; gap: 10px; }
        .nav-panel { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="fixed-header">
        <div style="font-size: 1.2rem;">🏠 <b>מתווך בקליק</b></div>
        <div style="font-size: 1.1rem;">👤 <b>{user_name}</b></div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<div class="centered-box">', unsafe_allow_html=True)
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות. | 2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
    st.write("6. ציון עובר: 60. | 7. חל איסור על שימוש בחומר עזר.")
    st.write("")
    c1, c2 = st.columns([2, 1])
    with c1: agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    with c2:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 2.8], gap="large")
    
    with col_nav:
        st.markdown('<div class="nav-panel">', unsafe_allow_html=True)
        rem = logic.get_remaining_seconds()
        st.markdown(f"""
            <div class="timer-display" id="js-timer">--:--</div>
            <script>
            var seconds = {rem};
            function up() {{
                var m = Math.floor(seconds/60), s = seconds%60;
                document.getElementById('js-timer').innerHTML = 
                    (m<10?"0":"")+m+":"+(s<10?"0":"")+s;
                if(seconds>0) seconds--;
            }}
            setInterval(up, 1000); up();
            </script>
        """, unsafe_allow_html=True)
        st.write("<b>ניווט:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    active = (idx <= st.session_state.max_reached)
                    if col.button(f"{idx}", key=f"v_{idx}", disabled=not active):
                        st.session_state.current_q = idx; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div class="exam-header-title">מבחן לרישוי מתווכים</div>', unsafe_allow_html=True)
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.subheader(f"שאלה {st.session_state.current_q}")
            st.write(q["question"])
            ans = st.radio("בחר תשובה:", q["options"], 
                           index=st.session_state.answers_user.get(st.session_state.current_q),
                           key=f"q_{st.session_state.current_q}")
            if ans is not None:
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(ans)
            st.divider()
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("הקודם", disabled=(st.session_state.current_q==1)):
                    logic.handle_navigation("prev"); st.rerun()
            with b2:
                can_next = (st.session_state.current_q in st.session_state.answers_user and st.session_state.current_q < 25)
                if st.button("הבא", disabled=not can_next):
                    logic.handle_navigation("next"); st.rerun()
            with b3:
                if 25 in st.session_state.answers_user:
                    if st.button("סיים בחינה"): st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"ציון סופי: {score}")
    for r in res:
        st.write(f"{'✅' if r['is_correct'] else '❌'} שאלה {r['num']}: {r['user_text']}")

# סוף קובץ
