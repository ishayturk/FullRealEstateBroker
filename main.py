# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V16 | Date: 22/02/2026 | 00:05
import streamlit as st
import logic
import time

# מצב סיידבר: נסתר בהסבר, פתוח בבחינה
s_state = "expanded" if ("step" in st.session_state and 
         st.session_state.step == "exam_run") else "collapsed"

st.set_page_config(page_title="מתווך בקליק", layout="wide", 
                   initial_sidebar_state=s_state)

user_name = st.query_params.get("user", "אורח")

# CSS לפתרון הריצוד והתאמה לנייד
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 800px !important; margin: auto !important; padding-top: 0.5rem !important; }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #eee;
    }
    
    /* הסתרת כפתור סגירת סיידבר למניעת ריצוד */
    [data-testid="sidebar-close-button"] { display: none !important; }
    
    /* התאמה לנייד */
    @media (max-width: 600px) {
        .fixed-header { flex-direction: column; align-items: flex-start; }
        [data-testid="stSidebar"] { display: none !important; }
        .mobile-timer { display: block !important; }
    }
    
    .timer-display {
        font-size: 1.5rem; font-weight: bold; color: #d32f2f;
        background: #fdf2f2; padding: 10px; border-radius: 8px;
        text-align: center; border: 1px solid #ffcdd2; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון
st.markdown(f"""
    <div class="fixed-header">
        <div>🏠 <b>מתווך בקליק - מערכת בחינות</b></div>
        <div style="color: #555;">👤 {user_name}</div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.markdown("1. 25 שאלות | 2. 90 דקות | 3. מעבר לאחר סימון | 4. חזרה לשאלות שנענו | 5. נעילה בסיום | 6. עובר: 60 | 7. ללא חומר עזר")
    if st.checkbox("אני מאשר את ההוראות"):
        if st.button("התחל בחינה"):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            logic.generate_question(2)
            st.rerun()

elif st.session_state.step == "exam_run":
    # הצגת טיימר בנייד (כי הסיידבר מוסתר)
    st.markdown(f'<div class="mobile-timer" style="display:none;"><div class="timer-display">⏳ {logic.get_timer_text()}</div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f'<div class="timer-display">{logic.get_timer_text()}</div>', unsafe_allow_html=True)
        st.write("מפת שאלות:")
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"n_{idx}", disabled=not is_active):
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

elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"ציון סופי: {score}")
    for r in res:
        st.write(f"{'✅' if r['is_correct'] else '❌'} שאלה {r['num']}: {r['user_text']}")

# סוף קובץ
