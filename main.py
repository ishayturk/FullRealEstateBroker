# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V09 | Date: 21/02/2026 | 23:45
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

# CSS - שחזור מדויק של העיצוב
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 800px !important; margin: auto !important; padding-top: 0.5rem !important; }
    
    .fixed-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
        border-bottom: 1px solid #eee;
    }
    
    .timer-container {
        background: #262730;
        color: #ffffff;
        padding: 15px;
        text-align: center;
        border-radius: 8px;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    [data-testid="stSidebar"] { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# שחזור כותרת הדף המקורית (סטריפ עליון)
st.markdown(f"""
    <div class="fixed-header">
        <div>
            <span style="font-size: 1.2rem; font-weight: bold;">🏠 מתווך בקליק - מערכת בחינות</span>
        </div>
        <div>
            👤 <b>{user_name}</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# קריאה לפונקציית האתחול
logic.initialize_exam()

if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות. 2. זמן מוקצב: 90 דקות. 3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו. 5. בסיום 90 דקות המבחן יינעל. 6. ציון עובר: 60. 7. חל איסור על שימוש בחומר עזר.")
    st.write("")
    col_c, col_b = st.columns([2, 1])
    with col_c: agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    with col_b:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            logic.generate_question(2)
            st.rerun()

elif st.session_state.step == "exam_run":
    if logic.check_exam_status():
        st.session_state.step = "time_up"; st.rerun()

    with st.sidebar:
        st.markdown(f'<div class="timer-container">{logic.get_timer_display()}</div>', unsafe_allow_html=True)
        st.write("ניווט:")
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"btn_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx; st.rerun()

    q_data = st.session_state.exam_data.get(st.session_state.current_q)
    if q_data:
        st.subheader(f"שאלה {st.session_state.current_q}")
        st.write(q_data["question"])
        choice = st.radio("בחר תשובה:", q_data["options"], 
                          index=st.session_state.answers_user.get(st.session_state.current_q), 
                          key=f"r_{st.session_state.current_q}")
        if choice:
            st.session_state.answers_user[st.session_state.current_q] = q_data["options"].index(choice)

        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("שאלה קודמת", disabled=(st.session_state.current_q == 1)):
                logic.handle_navigation("prev"); st.rerun()
        with c2:
            no_next = (st.session_state.current_q not in st.session_state.answers_user or st.session_state.current_q == 25)
            if st.button("שאלה הבאה", disabled=no_next):
                logic.handle_navigation("next"); st.rerun()
        with c3:
            if 25 in st.session_state.answers_user:
                if st.button("סיים בחינה"):
                    st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "time_up":
    st.header("הזמן לבחינה הסתיים")
    if st.button("סיים בחינה"): st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "summary":
    score, results = logic.get_results_data()
    st.header(f"ציון סופי: {score}")
    for res in results:
        sym = "✅" if res["is_correct"] else "❌"
        st.markdown(f"**{sym} שאלה {res['num']}**")
        st.write(f"תשובתך: {res['user_text']}")
        if not res["is_correct"]:
            st.markdown(f"*התשובה הנכונה:* {res['correct_text']}")
        st.write("---")

# סוף קובץ
