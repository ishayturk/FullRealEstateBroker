# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V19 | Date: 21/02/2026 | 23:55
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
    .block-container { max-width: 1200px !important; margin: auto !important; padding-top: 1rem !important; }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #eee; margin-bottom: 25px; flex-wrap: wrap;
    }
    
    .timer-box {
        text-align: center; background: #f8f9fa; border: 1px solid #ddd;
        padding: 12px; border-radius: 8px; font-weight: bold; font-size: 1.4rem;
        margin-bottom: 20px; color: #333;
    }

    @media (max-width: 600px) {
        .fixed-header { flex-direction: column; align-items: flex-start; }
        .nav-col-wrapper { display: none !important; }
        .mobile-timer { display: block !important; margin-bottom: 20px; }
    }
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון
st.markdown(f"""
    <div class="fixed-header">
        <div>🏠 <b>מתווך בקליק - מערכת בחינות</b></div>
        <div style="color: #666;">👤 משתמש: {user_name}</div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

# דף הסבר - שחזור מלא ומדויק
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
    st.write("6. ציון עובר: 60.")
    st.write("7. חל איסור על שימוש בחומר עזר.")
    st.write("")
    
    c_agree, c_start = st.columns([2, 1])
    with c_agree:
        agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    with c_start:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            logic.generate_question(2)
            st.rerun()

# דף בחינה - ניווט מימין, שאלות משמאל
elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 3])
    
    with col_nav:
        st.markdown(f'<div class="timer-box">⏳ {logic.get_timer_display()}</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-col-wrapper">', unsafe_allow_html=True)
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    is_active = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"nav_{idx}", disabled=not is_active):
                        st.session_state.current_q = idx; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        # טיימר לנייד בלבד
        st.markdown(f'<div class="mobile-timer" style="display:none;"><div class="timer-box">⏳ {logic.get_timer_display()}</div></div>', unsafe_allow_html=True)
        
        q_data = st.session_state.exam_data.get(st.session_state.current_q)
        if q_data:
            st.subheader(f"שאלה {st.session_state.current_q}")
            st.write(q_data["question"])
            ans = st.radio("בחר תשובה:", q_data["options"], 
                           index=st.session_state.answers_user.get(st.session_state.current_q),
                           key=f"ans_{st.session_state.current_q}")
            if ans:
                st.session_state.answers_user[st.session_state.current_q] = q_data["options"].index(ans)

            st.divider()
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("הקודם", disabled=(st.session_state.current_q==1)):
                    logic.handle_navigation("prev"); st.rerun()
            with b2:
                no_next = (st.session_state.current_q not in st.session_state.answers_user or st.session_state.current_q==25)
                if st.button("הבא", disabled=no_next):
                    logic.handle_navigation("next"); st.rerun()
            with b3:
                if 25 in st.session_state.answers_user:
                    if st.button("סיים בחינה"): st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"ציון סופי: {score}")
    for r in res:
        icon = "✅" if r['is_correct'] else "❌"
        st.write(f"{icon} שאלה {r['num']}: {r['user_text']}")

# סוף קובץ
