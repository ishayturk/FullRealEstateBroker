import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_next_question_if_needed

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide", initial_sidebar_state="expanded")

# --- CSS ממוקד לתיקון רכיבים ללא פגיעה במבנה הדף ---
st.markdown("""
    <style>
    /* יישור גלובלי לימין */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* מניעת גלילה מיותרת */
    .block-container { padding-top: 1.5rem !important; }

    /* רדיו באטן: נקודה מימין, מרווח ברור, ללא מסגרת חונקת */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 20px !important;
        padding: 10px 0 !important;
        border: none !important;
    }
    
    /* הדגשת הטקסט ליד הרדיו */
    [data-testid="stRadio"] p { font-weight: 500; }

    /* צ'קבוקס הסבר */
    [data-testid="stCheckbox"] {
        border: 1px solid #333;
        padding: 12px;
        margin: 15px 0;
        width: fit-content;
        border-radius: 5px;
    }

    /* שעון יציב וטבעי */
    .timer-display {
        text-align: center;
        font-family: sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #1e1e1e;
        background-color: #ffffff; /* רקע לבן נקי */
        margin-bottom: 10px;
    }
    
    /* צמצום רווחים בין השאלה לתשובות ולכפתורים */
    .stRadio { margin-top: -15px !important; }
    .stDivider { margin: 10px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    # ייצור שאלה 1 ברקע בזמן הקריאה
    fetch_next_question_if_needed()
    
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    <div style="direction: rtl; text-align: right; line-height: 1.8;">
        <ul>
            <li>לבחינה 25 שאלות אמריקאיות</li>
            <li>זמן הבחינה הוא 90 דקות</li>
            <li>ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה על השאלה הנוכחית</li>
            <li>ניתן לנווט בין השאלות שכבר ענית עליהן</li>
            <li>סיימת את הבחינה לחץ/י על כפתור סיים בחינה</li>
            <li>בתום הזמן המבחן מסתיים במיידי ולא תוכל להמשיך לנווט</li>
            <li>בסיום הבחינה תקבל משוב על הצלחתך</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    agreed = st.checkbox("קראתי ומאשר את תנאי הבחינה")
    if st.button("התחל בחינה", disabled=not agreed):
        state['current_index'] = 0
        state['start_time'] = time.time()
        # ייצור שאלה 2 מיד עם ההתחלה
        fetch_next_question_if_needed()
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # שעון JS ללא ריצוד
    timer_html = f"""
    <div class="timer-display" id="clock"></div>
    <script>
        var timeLeft = {remaining};
        function updateClock() {{
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            document.getElementById('clock').innerHTML = (m < 10 ? '0' : '') + m + ":" + (s < 10 ? '0' : '') + s;
            if (timeLeft > 0) {{ timeLeft--; setTimeout(updateClock, 1000); }}
            else {{ window.parent.location.reload(); }}
        }}
        updateClock();
    </script>
    """
    components.html(timer_html, height=75)

    # סידבר לניווט
    with st.sidebar:
        st.write("### ניווט שאלות")
        for i in range(0, 25, 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx < 25:
                    is_ready = idx < len(state['questions'])
                    if cols[j].button(f"{idx+1}", key=f"nav_{idx}", disabled=not is_ready):
                        state['current_index'] = idx
                        st.rerun()

    # הצגת השאלה מהזיכרון
    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.markdown(f"#### {q['question_text']}")
        
        current_ans = state['answers'].get(state['current_index'], None)
        choice = st.radio("בחר תשובה:", q['options'], index=current_ans, key=f"radio_{state['current_index']}", label_visibility="collapsed")
        
        if choice is not None:
            state['answers'][state['current_index']] = q['options'].index(choice)

        st.divider()
        
        # כפתורי פעולה
        col_next, col_finish, col_prev = st.columns([1,1,1])
        with col_prev:
            if state['current_index'] > 0:
                if st.button("שאלה קודמת ➡️"):
                    state['current_index'] -= 1
                    st.rerun()
        with col_finish:
            if state['current_index'] == 24 or len(state['answers']) >= 25:
                if st.button("🏁 סיים בחינה"):
                    state['is_finished'] = True
                    st.rerun()
        with col_next:
            if state['current_index'] < 24:
                can_go_next = state['current_index'] in state['answers']
                if st.button("⬅️ שאלה הבאה", disabled=not can_go_next):
                    state['current_index'] += 1
                    # Prefetch לשאלה הבאה בתור
                    fetch_next_question_if_needed()
                    st.rerun()
    else:
        st.info("מכין את השאלה... מיד מתחילים")
        fetch_next_question_if_needed()
        st.rerun()

# --- עמוד סיום ---
else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות מתוך 25.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
