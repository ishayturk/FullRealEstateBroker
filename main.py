# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V24 | Date: 22/02/2026 | 00:30
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
    
    /* הגבלת רוחב ל-50% ומירכוז */
    .block-container { 
        max-width: 800px !important; 
        margin: auto !important; 
        padding-top: 2rem !important; 
    }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #eee; margin-bottom: 40px;
    }
    
    .nav-panel {
        background-color: #f4f4f4; border: 1px solid #ddd; padding: 15px;
        border-radius: 10px;
    }
    
    .timer-display {
        text-align: center; background: #fff; border: 1px solid #ccc;
        padding: 8px; border-radius: 5px; font-weight: bold;
        font-size: 1.4rem; color: #d32f2f; margin-bottom: 15px;
    }

    .centered-box { 
        max-width: 600px; margin: 100px auto; text-align: right; 
    }
    
    .exam-title-main {
        font-size: 1.6rem; font-weight: bold; color: #333;
        text-align: center; margin-bottom: 5px;
    }
    
    .exam-subtitle {
        font-size: 1.1rem; color: #666; text-align: center;
        margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;
    }

    @media (max-width: 600px) {
        .block-container { max-width: 95% !important; }
        .fixed-header { flex-direction: column; gap: 10px; }
        .nav-panel { display: none !important; }
    }
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון נקי
st.markdown(f"""
    <div class="fixed-header">
        <div style="font-size: 1.2rem;">🏠 <b>מתווך בקליק</b></div>
        <div style="font-size: 1.1rem;">👤 <b>{user_name}</b></div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

# דף הסבר - 7 סעיפים מלאים וממורכזים
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
    c1, c2 = st.columns([2, 1])
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
        rem = logic.get_remaining_seconds()
        st.markdown(f"""
            <div class="timer-display" id="js-timer">--:--</div>
            <script>
            var s = {rem};
            function up() {{
                var m=Math.floor(s/60), sec=s%60;
                document.getElementById('js-timer').innerHTML=(m<10?"0":"")+m+":"+(sec<10?"0":"")+sec;
                if(s>0) s--;
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
                    act = (idx <= st.session_state.max_reached)
                    if col.button(f"{idx}", key=f"n_{idx}", disabled=not act):
                        st.session_state.current_q = idx; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div class="exam-title-main">מבחן רישוי למתווכים</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exam-subtitle">שאלה {st.session_state.current_q} מתוך 25</div>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
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
