# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V26 | Date: 22/02/2026 | 00:55
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1000px !important; margin: auto !important; padding-top: 1rem !important; }
    
    .fixed-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; margin-bottom: 20px; width: 100%;
    }
    
    .nav-panel { background-color: #f7f8f9; border: 1px solid #e1e4e8; padding: 20px; border-radius: 12px; }
    
    .timer-display {
        text-align: center; background: #ffffff; border: 1px solid #ddd;
        padding: 10px; border-radius: 8px; font-weight: bold;
        font-size: 1.6rem; color: #333; margin-bottom: 20px;
    }

    .q-link { 
        display: inline-block; width: 35px; text-align: center; margin: 5px;
        font-size: 1.1rem; font-weight: bold; text-decoration: none;
    }
    .q-active { color: #007bff; cursor: pointer; border-bottom: 2px solid #007bff; }
    .q-disabled { color: #ccc; cursor: default; }

    .centered-box { max-width: 700px; margin: 20px auto; }
    .exam-title-main { font-size: 1.8rem; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .exam-subtitle { font-size: 1.1rem; color: #555; text-align: center; border-bottom: 1px solid #eee; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# סטריפ עליון ממורכז
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
    for i, txt in enumerate(["המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.", 
                             "ניתן לחזור אחורה רק לשאלות שנענו.", "בסיום 90 דקות המבחן יינעל.", 
                             "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."], 1):
        st.write(f"{i}. {txt}")
    st.write("")
    c1, c2 = st.columns([1.5, 1])
    with c1: agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
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
        st.markdown(f'<div class="timer-display" id="t-box">00:00</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <script>
            var s = {rem};
            function up() {{
                var m=Math.floor(s/60), sec=s%60;
                document.getElementById('t-box').innerHTML=(m<10?"0":"")+m+":"+(sec<10?"0":"")+sec;
                if(s>0) s--;
            }}
            setInterval(up, 1000); up();
            </script>
        """, unsafe_allow_html=True)
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        # ניווט מספרים נקי למניעת קומות
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    if idx <= st.session_state.max_reached:
                        if cols[i].button(str(idx), key=f"n_{idx}"):
                            st.session_state.current_q = idx; st.rerun()
                    else:
                        cols[i].markdown(f"<span style='color:#ccc; display:block; text-align:center;'>{idx}</span>", unsafe_allow_html=True)
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
            if ans: st.session_state.answers_user[st.session_state.current_q] = q["options"].index(ans)
            st.divider()
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("שאלה קודמת", disabled=(st.session_state.current_q==1)):
                    logic.handle_navigation("prev"); st.rerun()
            with b2:
                can = (st.session_state.current_q in st.session_state.answers_user and st.session_state.current_q < 25)
                if st.button("שאלה הבאה", disabled=not can):
                    logic.handle_navigation("next"); st.rerun()
            with b3:
                if 25 in st.session_state.answers_user:
                    if st.button("סיום וציון"): st.session_state.step = "summary"; st.rerun()

elif st.session_state.step == "summary":
    score, res = logic.get_results_data()
    st.header(f"ציון סופי: {score}")

# סוף קובץ
