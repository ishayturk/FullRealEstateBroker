import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_and_store_question

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide", initial_sidebar_state="expanded")

# CSS לתיקון יישור, רדיו, צ'קבוקס וצמצום רווחים
st.markdown("""
    <style>
    /* יישור RTL גלובלי */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* צמצום רווחים בראש הדף למניעת גלילה */
    .block-container { padding-top: 1rem !important; padding-bottom: 0 !important; }
    
    /* יישור רדיו: נקודה מימין למלל ללא מסגרת חונקת */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 15px !important;
        padding: 5px 0 !important;
        border: none !important;
    }

    /* צ'קבוקס בעמוד ההסבר */
    [data-testid="stCheckbox"] {
        border: 1px solid #000;
        padding: 10px;
        margin: 10px 0;
        width: fit-content;
    }

    /* שעון בולט עם רקע לבן */
    .timer-container {
        text-align: center;
        font-family: sans-serif;
        font-size: 38px;
        font-weight: bold;
        color: #333;
        background-color: white;
        padding: 5px;
        border: 1px solid #eee;
        border-radius: 8px;
    }

    /* צמצום המרווח לפני כפתורי הניווט */
    .stDivider { margin: 0.5rem 0 !important; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר לבחינה ---
if state['current_index'] == -1:
    # ייצור שאלה ראשונה ברקע בזמן הקריאה
    if not state['questions']:
        fetch_and_store_question()
        
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    <div style="direction: rtl; text-align: right;">
        <ul>
            <li>לבחינה 25 שאלות אמריקאיות</li>
            <li>זמן הבחינה הוא 90 דקות</li>
            <li>ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה</li>
            <li>ניתן לנווט בין שאלות שכבר ענית עליהן</li>
            <li>בסיום הזמן המבחן ננעל אוטומטית</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    agreed = st.checkbox("קראתי ומאשר")
    if st.button("התחל בחינה", disabled=not agreed):
        state['current_index'] = 0
        state['start_time'] = time.time()
        # ייצור שאלה 2 מיד עם ההתחלה
        fetch_and_store_question()
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # שעון שקט (ללא ריצוד התפריט)
    timer_html = f"""
    <div class="timer-container" id="timer"></div>
    <script>
        var seconds = {remaining};
        function updateTimer() {{
            var m = Math.floor(seconds / 60);
            var s = seconds % 60;
            document.getElementById('timer').innerHTML = (m < 10 ? '0' : '') + m + ":" + (s < 10 ? '0' : '') + s;
            if (seconds > 0) {{ seconds--; setTimeout(updateTimer, 1000); }}
            else {{ window.parent.location.reload(); }}
        }}
        updateTimer();
    </script>
    """
    components.html(timer_html, height=70)

    # סידבר - 4 בשורה
    with st.sidebar:
        st.write("### ניווט")
        for i in range(0, 25, 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx < 25:
                    can_nav = idx < len(state['questions'])
                    if cols[j].button(f"{idx+1}", key=f"n_{idx}", disabled=not can_nav):
                        state['current_index'] = idx
                        st.rerun()

    # הצגת שאלה (היא כבר בזיכרון בזכות ה-Prefetch)
    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.markdown(f"**{q['question_text']}**")
        
        ans = state['answers'].get(state['current_index'], None)
        choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
        
        if choice is not None:
            state['answers'][state['current_index']] = q['options'].index(choice)

        st.divider()
        
        # כפתורי ניווט
        c_next, c_finish, c_prev = st.columns([1,1,1])
        with c_prev:
            if state['current_index'] > 0:
                if st.button("שאלה קודמת ➡️"):
                    state['current_index'] -= 1
                    st.rerun()
        with c_finish:
            if state['current_index'] == 24 or len(state['answers']) >= 25:
                if st.button("🏁 סיים בחינה"):
                    state['is_finished'] = True
                    st.rerun()
        with c_next:
            if state['current_index'] < 24:
                has_ans = state['current_index'] in state['answers']
                if st.button("⬅️ שאלה הבאה", disabled=not has_ans):
                    state['current_index'] += 1
                    # ייצור השאלה הבאה (Prefetch) רק אם היא עוד לא קיימת
                    if len(state['questions']) <= state['current_index'] + 1:
                        fetch_and_store_question()
                    st.rerun()
    else:
        st.info("מייצר שאלה... (זה קורה רק אם הניווט היה מהיר מה-AI)")
        fetch_and_store_question()
        st.rerun()

# --- עמוד סיום ---
else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
