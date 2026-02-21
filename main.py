# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V13 | Date: 21/02/2026 | 23:40
import streamlit as st
import logic
import time

# הגדרת מצב סיידבר קבוע לפי שלב
if "step" in st.session_state and st.session_state.step == "exam_run":
    s_state = "expanded"
else:
    s_state = "collapsed"

st.set_page_config(page_title="מתווך בקליק", layout="wide", 
                   initial_sidebar_state=s_state)

user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 800px !important; margin: auto !important; padding-top: 0.5rem !important; }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #eee;
    }
    
    /* טיימר קטן וסולידי */
    .timer-text {
        color: #444; font-size: 1.2rem; font-weight: bold;
        text-align: center; background: #f0f2f6;
        padding: 5px; border-radius: 4px; border: 1px solid #ddd;
    }
    
    [data-testid="stSidebar"] { direction: rtl; }
    /* ביטול כפתור הסגירה של הסיידבר למניעת שינוי ע"י משתמש */
    [data-testid="sidebar-close-button"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון
st.markdown(f'<div class="fixed-header"><div>🏠 <b>מתווך בקליק</b></div><div>👤 <b>{user_name}</b></div></div>', unsafe_allow_html=True)

logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן")
    st.write("מבחן מקצועי - 25 שאלות, 90 דקות.")
    if st.checkbox("אני מוכן"):
        if st.button("התחל"):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            logic.generate_question(2)
            st.rerun()

elif st.session_state.step == "exam_run":
    if logic.check_exam_status():
        st.session_state.step = "time_up"; st.rerun()

    with st.sidebar:
        # שימוש ב-empty למניעת רעידות
        t_placeholder = st.empty()
        t_placeholder.markdown(f'<div class="timer-text">{logic.get_timer_display()}</div>', unsafe_allow_html=True)
        
        st.write("ניווט:")
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    is_act = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"v_{idx}", disabled=not is_act):
                        st.session_state.current_q = idx; st.rerun()
        
        # רענון אוטומטי כל 10 שניות כדי לא להכביד אך לשמור על טיימר חי
        time.sleep(0.1) 
        if int(time.time()) % 10 == 0: st.rerun()

    q_data = st.session_state.exam_data.get(st.session_state.current_q)
    if q_data:
        st.subheader(f"שאלה {st.session_state.current_q}")
        st.write(q_data["question"])
        ans = st.radio("תשובה:", q_data["options"], 
                       index=st.session_state.answers_user.get(st.session_state.current_q),
                       key=f"rd_{st.session_state.current_q}")
        if ans:
            st.session_state.answers_user[st.session_state.current_q] = q_data["options"].index(ans)

        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1: 
            if st.button("הקודם", disabled=(st.session_state.current_q==1)):
                logic.handle_navigation("prev"); st.rerun()
        with c2:
            if st.button("הבא", disabled=(st.session_state.current_q not in st.session_state.answers_user or st.session_state.current_q==25)):
                logic.handle_navigation("next"); st.rerun()
        with c3:
            if 25 in st.session_state.answers_user:
                if st.button("סיים"): st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"ציון: {score}")
    for r in res:
        st.write(f"{'✅' if r['is_correct'] else '❌'} שאלה {r['num']}: {r['user_text']}")

# סוף קובץ
