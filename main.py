# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V15 | Date: 21/02/2026 | 23:55
import streamlit as st
import logic
import time

# מצב סיידבר: נסתר בנייד, פתוח במחשב
st.set_page_config(page_title="מתווך בקליק", layout="wide", 
                   initial_sidebar_state="expanded")

user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 800px !important; margin: auto !important; padding-top: 0.5rem !important; }
    
    /* סטריפ עליון אדפטיבי */
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #eee; flex-wrap: wrap;
    }
    
    @media (max-width: 600px) {
        .fixed-header { flex-direction: column; align-items: flex-start; }
        [data-testid="stSidebar"] { display: none !important; }
    }
    
    /* קיבוע סיידבר במחשב */
    [data-testid="sidebar-close-button"] { display: none !important; }
    
    .timer-container {
        text-align: center; background: #f8f9fa; border: 1px solid #ddd;
        padding: 10px; border-radius: 5px; margin-bottom: 20px;
    }
    #timer-val { font-size: 1.4rem; font-weight: bold; color: #333; }
    </style>
""", unsafe_allow_html=True)

# הצגת הסטריפ העליון
st.markdown(f"""
    <div class="fixed-header">
        <div>🏠 <b>מתווך בקליק - מערכת בחינות</b></div>
        <div style="color: #666; font-size: 0.9rem;">👤 משתמש: {user_name}</div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

# דף הסבר - שחזור מלא
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.markdown("""
    1. המבחן כולל 25 שאלות.
    2. זמן מוקצב: 90 דקות.
    3. מעבר לשאלה הבאה רק לאחר סימון תשובה.
    4. ניתן לחזור אחורה רק לשאלות שנענו.
    5. בסיום 90 דקות המבחן יינעל.
    6. ציון עובר: 60.
    7. חל איסור על שימוש בחומר עזר.
    """)
    st.write("")
    if st.checkbox("קראתי את ההוראות ואני מוכן להתחיל"):
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            logic.generate_question(2)
            st.rerun()

# דף בחינה
elif st.session_state.step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    
    with st.sidebar:
        st.markdown(f"""
            <div class="timer-container">
                <div id="timer-val"></div>
            </div>
            <script>
            var seconds = {rem_sec};
            function updateTimer() {{
                var mins = Math.floor(seconds / 60);
                var secs = seconds % 60;
                document.getElementById('timer-val').innerHTML = 
                    (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
                if (seconds > 0) {{ seconds--; }}
            }}
            setInterval(updateTimer, 1000);
            updateTimer();
            </script>
        """, unsafe_allow_html=True)
        
        st.write("ניווט:")
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"nav_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx; st.rerun()

    q_data = st.session_state.exam_data.get(st.session_state.current_q)
    if q_data:
        st.subheader(f"שאלה {st.session_state.current_q}")
        st.write(q_data["question"])
        ans = st.radio("בחר תשובה:", q_data["options"], 
                       index=st.session_state.answers_user.get(st.session_state.current_q),
                       key=f"q_{st.session_state.current_q}")
        if ans:
            st.session_state.answers_user[st.session_state.current_q] = q_data["options"].index(ans)

        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("הקודם", disabled=(st.session_state.current_q==1)):
                logic.handle_navigation("prev"); st.rerun()
        with c2:
            no_next = (st.session_state.current_q not in st.session_state.answers_user or st.session_state.current_q==25)
            if st.button("הבא", disabled=no_next):
                logic.handle_navigation("next"); st.rerun()
        with c3:
            if 25 in st.session_state.answers_user:
                if st.button("סיים בחינה"): st.session_state.step = "summary"; st.rerun()

# דף סיכום
elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"ציון סופי: {score}")
    for r in res:
        icon = "✅" if r['is_correct'] else "❌"
        st.markdown(f"**{icon} שאלה {r['num']}**")
        st.write(f"תשובתך: {r['user_text']}")
        if not r['is_correct']:
            st.markdown(f"*התשובה הנכונה:* {r['correct_text']}")
        st.write("---")

# סוף קובץ
