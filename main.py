# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V34 | Date: 22/02/2026 | 09:40
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* הגדרות בסיס */
    * { direction: rtl; }
    header, #MainMenu, footer { visibility: hidden; }
    
    /* קונטיינר ראשי */
    .block-container {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding-top: 1rem !important;
    }
    
    /* סטריפ עליון קבוע */
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        padding: 10px 0;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 30px;
    }

    .nav-panel { 
        background-color: #f8f9fa; 
        border: 1px solid #e1e4e8; 
        padding: 20px; 
        border-radius: 12px; 
    }
    
    .timer-display {
        text-align: center; background: #fff; border: 1px solid #333;
        padding: 8px; border-radius: 8px; font-weight: bold;
        font-size: 1.5rem; color: #333; margin-bottom: 15px; font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# הצגת הסטריפ העליון - תמיד בראש הדף
st.markdown(f"""
    <div class="header-box">
        <div style="font-size: 1.3rem;">🏠 <b>מתווך בקליק</b></div>
        <div style="font-size: 1.2rem;">👤 <b>{user_name}</b></div>
    </div>
""", unsafe_allow_html=True)

logic.initialize_exam()

# דף הוראות - שימוש בעמודות למירכוז עצמאי
if "step" not in st.session_state or st.session_state.step == "instructions":
    _, center_col, _ = st.columns([1, 4, 1])
    
    with center_col:
        st.markdown('<h1 style="text-align: center;">הוראות למבחן רישויי מקרקעין</h1>', unsafe_allow_html=True)
        
        instructions = [
            "המבחן כולל 25 שאלות.", "זמן מוקצב: 90 דקות.", "מעבר לשאלה הבאה רק לאחר סימון תשובה.",
            "ניתן לחזור אחורה רק לשאלות שנענו.", "בסיום 90 דקות המבחן יינעל.",
            "ציון עובר: 60.", "חל איסור על שימוש בחומר עזר."
        ]
        for i, txt in enumerate(instructions, 1):
            st.write(f"{i}. {txt}")
        
        st.write("")
        # מירכוז אלמנטי הבחירה והכפתור
        agree = st.checkbox("קראתי את ההוראות")
        if st.button("התחל בחינה", disabled=not agree, use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"; st.rerun()

elif st.session_state.step == "exam_run":
    col_nav, col_main = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        st.markdown('<div class="nav-panel">', unsafe_allow_html=True)
        rem = logic.get_remaining_seconds()
        st.markdown(f'<div class="timer-display" id="timer-v34">--:--</div>', unsafe_allow_html=True)
        
        st.write("<b>מפת שאלות:</b>", unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = r + i + 1
                if idx <= 25:
                    if idx <= st.session_state.max_reached:
                        if cols[i].button(str(idx), key=f"btn_{idx}"):
                            st.session_state.current_q = idx; st.rerun()
                    else:
                        cols[i].markdown(f"<div style='color:#ccc; text-align:center; padding-top:5px;'>{idx}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main:
        st.markdown('<div style="text-align: center;"><h2 style="margin:0;">מבחן רישוי למתווכים</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #555;">שאלה {st.session_state.current_q} מתוך 25</p></div>', unsafe_allow_html=True)
        
        q = st.session_state.exam_data.get(st.session_state.current_q)
        if q:
            st.markdown(f"#### {q['question']}")
            ans = st.radio("בחר תשובה:", q["options"], 
                           index=st.session_state.answers_user.get(st.session_state.current_q),
                           key=f"radio_{st.session_state.current_q}")
            if ans: 
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
                    if st.button("סיום בחינה"): st.session_state.step = "summary"; st.rerun()

# סוף קובץ
