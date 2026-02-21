# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V08 | Date: 21/02/2026 | 23:30
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 800px !important; margin: auto !important; padding-top: 0.5rem !important; }
    .fixed-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 1px solid #eee; }
    [data-testid="stSidebar"] { direction: rtl; background-color: #f9f9f9; }
    .timer-display { background: #333; color: #0f0; padding: 10px; text-align: center; font-size: 1.8rem; font-family: monospace; border-radius: 5px; margin-bottom: 15px; }
    .stRadio > label { direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

# כותרת עליונה קבועה
st.markdown(f'<div class="fixed-header"><div>🏠 <b>מתווך בקליק</b></div><div>👤 <b>{user_name}</b></div></div>', unsafe_allow_html=True)

logic.initialize_exam()

# דף הסבר - ללא שינוי מהמקור
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות. 2. זמן מוקצב: 90 דקות. 3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו. 5. בסיום 90 דקות המבחן יינעל. 6. ציון עובר: 60. 7. חל איסור על שימוש בחומר עזר.")
    st.write("")
    c_check, c_btn = st.columns([2, 1])
    with c_check: agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    with c_btn:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            logic.generate_question(2)
            st.rerun()

# דף בחינה
elif st.session_state.step == "exam_run":
    if logic.check_exam_status():
        st.session_state.step = "time_up"; st.rerun()

    with st.sidebar:
        st.markdown(f'<div class="timer-display">{logic.get_timer_display()}</div>', unsafe_allow_html=True)
        st.write("ניווט שאלות (1-25):")
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    # כפתור אקטיבי אם ענה או אם זו השאלה הנוכחית
                    is_act = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"s_{idx}", disabled=not is_act):
                        st.session_state.current_q = idx; st.rerun()

    q_data = st.session_state.exam_data.get(st.session_state.current_q)
    if q_data:
        st.title(f"שאלה {st.session_state.current_q}")
        st.write(q_data["question"])
        choice = st.radio("בחר תשובה:", q_data["options"], 
                          index=st.session_state.answers_user.get(st.session_state.current_q), 
                          key=f"q_radio_{st.session_state.current_q}")
        if choice:
            st.session_state.answers_user[st.session_state.current_q] = q_data["options"].index(choice)

        st.divider()
        n1, n2, n3 = st.columns(3)
        with n1:
            if st.button("שאלה קודמת", disabled=(st.session_state.current_q == 1)):
                logic.handle_navigation("prev"); st.rerun()
        with n2:
            next_off = (st.session_state.current_q not in st.session_state.answers_user or st.session_state.current_q == 25)
            if st.button("שאלה הבאה", disabled=next_off):
                logic.handle_navigation("next"); st.rerun()
        with n3:
            if 25 in st.session_state.answers_user:
                if st.button("סיים בחינה"):
                    st.session_state.step = "summary"; st.rerun()

# דף סיום זמן
elif st.session_state.step == "time_up":
    st.header("הזמן לבחינה הסתיים")
    if st.button("סיים בחינה"): st.session_state.step = "summary"; st.rerun()

# דף משוב
elif st.session_state.step == "summary":
    score, results = logic.get_results_data()
    st.title(f"ציון סופי: {score}")
    st.divider()
    for res in results:
        icon = "✅" if res["is_correct"] else "❌"
        color = "green" if res["is_correct"] else "red"
        st.markdown(f"**{icon} שאלה {res['num']}**")
        st.markdown(f"תשובתך: {res['user_text']}")
        if not res["is_correct"]:
            st.markdown(f"**התשובה הנכונה:** {res['correct_text']}")
        st.write("---")

# סוף קובץ
