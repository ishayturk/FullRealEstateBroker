# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Version: V06 | Date: 21/02/2026 | 23:55
import streamlit as st
import logic
import time

st.set_page_config(page_title="מתווך בקליק - בחינה", layout="wide", initial_sidebar_state="collapsed")

# 1. קליטת שם משתמש מה-URL
user_name = st.query_params.get("user", "אורח")

# 2. עיצוב CSS - צמצום רווחים ויישור
st.markdown("""
    <style>
    * { direction: rtl; text-align: right; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* מרכוז התוכן */
    .block-container { 
        max-width: 800px !important; 
        margin: auto !important; 
        padding-top: 0.5rem !important;
    }
    
    /* הסטריפ העליון */
    .fixed-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
    }

    /* העלאת התוכן שורה אחת למעלה כלפי הכותרת */
    .main-content {
        margin-top: 1rem;
    }
    
    /* יישור אלמנטים בשורה של הצ'קבוקס והכפתור */
    [data-testid="column"] {
        display: flex;
        align-items: center;
    }
    
    h1 {
        margin-bottom: 0.8rem !important;
    }

    /* טיימר מקובע לנייד/מחשב */
    .sticky-timer {
        position: fixed;
        top: 45px;
        right: 0;
        left: 0;
        background-color: #f0f2f6;
        text-align: center;
        padding: 5px;
        font-weight: bold;
        z-index: 1000;
        border-bottom: 1px solid #ddd;
    }

    /* רדיו בטאן מימין לטקסט */
    div[role="radiogroup"] {
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# 3. הכותרת
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

# אתחול לוגיקה
logic.initialize_exam()

# 4. דף ההסבר
if "step" not in st.session_state or st.session_state.step == "instructions":
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.title("הוראות למבחן רישויי מקרקעין")
    st.write("1. המבחן כולל 25 שאלות.")
    st.write("2. זמן מוקצב: 90 דקות.")
    st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
    st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
    st.write("5. בסיום 90 דקות המבחן יינעל.")
    st.write("6. ציון עובר: 60.")
    st.write("7. חל איסור על שימוש בחומר עזר.")
    
    st.write("") # שורת רווח בודדת
    
    # שורה אחת לצ'קבוקס ולכפתור
    col_checkbox, col_button = st.columns([2, 1])
    
    with col_checkbox:
        agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    
    with col_button:
        if st.button("התחל בחינה", disabled=not agree):
            st.session_state.start_time = time.time()
            st.session_state.step = "exam_run"
            # טעינה מוקדמת של שאלה 2 ברגע הלחיצה
            logic.generate_question(2)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# עמוד המבחן
elif st.session_state.step == "exam_run":
    # בדיקת זמן
    if logic.check_exam_status():
        st.session_state.step = "time_up"
        st.rerun()

    # סיידבר ניווט (מוצג רק בזמן בחינה)
    with st.sidebar:
        st.markdown(f'<div class="sticky-timer">זמן נותר: {logic.get_timer_display()}</div>', unsafe_allow_html=True)
        st.write("---")
        st.write("ניווט מהיר:")
        for row in range(0, 25, 4):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                idx = row + i + 1
                if idx <= 25:
                    # כפתור אקטיבי אם ענה עליה או שזו הנוכחית
                    active = idx in st.session_state.answers_user or idx == st.session_state.current_q
                    if col.button(f"{idx}", key=f"side_{idx}", disabled=not active):
                        st.session_state.current_q = idx
                        st.rerun()

    # הצגת השאלה הנוכחית
    q_num = st.session_state.current_q
    q_data = st.session_state.exam_data.get(q_num)

    if q_data:
        st.subheader(f"שאלה {q_num}")
        st.write(q_data["question"])
        
        # בחירת תשובה
        choice = st.radio("בחר תשובה:", q_data["options"], 
                          index=st.session_state.answers_user.get(q_num), 
                          key=f"r_{q_num}")
        
        if choice is not None:
            st.session_state.answers_user[q_num] = q_data["options"].index(choice)

        st.divider()
        
        # כפתורי ניווט
        c_prev, c_next, c_finish = st.columns(3)
        with c_prev:
            if st.button("שאלה קודמת", disabled=(q_num == 1)):
                logic.handle_navigation("prev")
                st.rerun()
        with c_next:
            # אקטיבי רק אם סומנה תשובה וזו לא שאלה 25
            next_disabled = (q_num not in st.session_state.answers_user) or (q_num == 25)
            if st.button("שאלה הבאה", disabled=next_disabled):
                logic.handle_navigation("next")
                st.rerun()
        with c_finish:
            # כפתור סיים בחינה מופיע אחרי תשובה לשאלה 25 ונשאר קבוע
            if 25 in st.session_state.answers_user:
                if st.button("סיים בחינה"):
                    st.session_state.step = "summary"
                    st.rerun()

# עמוד סיום זמן
elif st.session_state.step == "time_up":
    st.header("הזמן לבחינה הסתיים")
    st.write("לסיום הבחינה לחץ:")
    if st.button("סיים בחינה"):
        st.session_state.step = "summary"
        st.rerun()

# עמוד משוב (סיכום)
elif st.session_state.step == "summary":
    st.header("תוצאות הבחינה")
    st.write("דף משוב בבנייה...")

# סוף קובץ
