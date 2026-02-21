# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V25 | Date: 22/02/2026 | 00:45
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
    
    .block-container { 
        max-width: 1000px !important; 
        margin: auto !important; 
        padding-top: 1rem !important; 
    }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; margin-bottom: 20px;
    }
    
    .nav-panel {
        background-color: #f7f8f9; border: 1px solid #e1e4e8; 
        padding: 20px; border-radius: 12px;
    }
    
    .timer-display {
        text-align: center; background: #ffffff; border: 2px solid #eee;
        padding: 10px; border-radius: 8px; font-weight: bold;
        font-size: 1.6rem; color: #e63946; margin-bottom: 20px;
        font-family: monospace;
    }

    .centered-box { 
        max-width: 700px; margin: 20px auto; text-align: right; 
    }
    
    .exam-header-container {
        text-align: center; margin-bottom: 25px;
    }
    
    .exam-title-main {
        font-size: 1.8rem; font-weight: bold; color: #1a1a1a; margin-bottom: 5px;
    }
    
    .exam-subtitle {
        font-size: 1.1rem; color: #555;
        padding-bottom: 10px; border-bottom: 1px solid #f0f0f0;
    }

    @media (max-width: 600px) {
        .block-container { max-width: 100% !important; }
        .fixed-header { flex-direction: column; gap: 10px; }
        .nav-panel { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון ללא קו מפריד
st.markdown(f"""
    <div class="fixed-header">
        <div style="font-size: 1.3rem;">🏠 <b>מתווך בקליק</b></div>
        <div style="font-size: 1.2rem;">👤 <b>{user_name}</b></div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

# דף הסבר - צמוד למעלה עם 7 סעיפים
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<div class="centered-box">', unsafe_allow_html=True)
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
    st.write("6. ציון עובר: 60.")
    st.write("7. חל איסור על שימוש בחומר עזר.")
    st.write("")
    c1, c2 = st.columns([1.5, 1])
    with c1: agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    with c2:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# דף בחינה
elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        st.markdown('<div class="nav-panel">', unsafe_allow_html=True)
        rem_s = logic.get_remaining_seconds()
        st.markdown(f"""
            <div class="timer-display" id="timer-box">00:00</div>
            <script>
            var s = {rem_s};
            function tick() {{
                var m = Math.floor(s/60), sec = s%60;
                document.getElementById('timer-box').innerHTML = 
                    (m<10?"0":"")+m+":"+(sec<10?"0":"")+sec;
                if(s > 0) s--;
            }}
            setInterval(tick, 1000); tick();
            </script>
        """, unsafe_allow_html=True)
        
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = r + i + 1
                if idx <= 25:
                    # אקטיבי רק אם כבר לחצו "הבא" או אם זו השאלה הנוכחית
                    act = (idx <= st.session_state.max_reached)
                    if col.button(f"{idx}", key=f"btn_{idx}", disabled=not act):
                        st.session_state.current_q = idx; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div class="exam-header-container">', unsafe_allow_html=True)
        st.markdown('<div class="exam-title-main">מבחן רישוי למתווכים</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exam-subtitle">שאלה {st.session_state.current_q} מתוך 25</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f"#### {q['question']}")
            ans = st.radio("בחר את התשובה הנכונה ביותר:", q["options"], 
                           index=st.session_state.answers_user.get(st.session_state.current_q),
                           key=f"radio_{st.session_state.current_q}")
            if ans is not None:
                st.session_state.answers_user[st.session_state.current_q] = q["options"].index(ans)
            
            st.write("")
            st.divider()
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("שאלה קודמת", disabled=(st.session_state.current_q==1)):
                    logic.handle_navigation("prev"); st.rerun()
            with b2:
                # כפתור "הבא" פותח את השאלה הבאה בניווט
                can_go_next = (st.session_state.current_q in st.session_state.answers_user and st.session_state.current_q < 25)
                if st.button("שאלה הבאה", disabled=not can_go_next):
                    logic.handle_navigation("next"); st.rerun()
            with b3:
                if 25 in st.session_state.answers_user:
                    if st.button("סיום בחינה וקבלת ציון"): 
                        st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"תוצאות הבחינה: {score}/100")
    for r in res:
        st.write(f"{'✅' if r['is_correct'] else '❌'} שאלה {r['num']}: {r['user_text']}")

# סוף קובץ
