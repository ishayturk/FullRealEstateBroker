import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_and_store_question

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide", initial_sidebar_state="expanded")

# CSS לתיקון יישור, רדיו וצמצום רווחים
st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    .block-container { padding-top: 1rem !important; padding-bottom: 0 !important; }
    
    /* רדיו מימין למלל ללא מסגרת */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 20px !important;
        padding: 8px 0 !important;
    }

    [data-testid="stCheckbox"] {
        border: 1px solid #000;
        padding: 10px;
        width: fit-content;
    }

    .timer-container {
        text-align: center;
        font-family: sans-serif;
        font-size: 38px;
        font-weight: bold;
        color: #333;
        background-color: white;
        padding: 5px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    if not state['questions']:
        fetch_and_store_question()
        
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    <div style="direction: rtl; text-align: right;">
        <ul>
            <li>לבחינה 25 שאלות אמריקאיות</li>
            <li>זמן הבחינה הוא 90 דקות</li>
            <li>בסיום הזמן המבחן ננעל אוטומטית</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    agreed = st.checkbox("קראתי ומאשר")
    if st.button("התחל בחינה", disabled=not agreed):
        state['current_index'] = 0
        state['start_time'] = time.time()
        fetch_and_store_question() # הכנת שאלה 2
        st.rerun()

# --- עמוד בחינה ---
elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

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

    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.markdown(f"**{q['question_text']}**")
        
        ans = state['answers'].get(state['current_index'], None)
        choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
        
        if choice is not None:
            state['answers'][state['current_index']] = q['options'].index(choice)

        st.divider()
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
                    if len(state['questions']) <= state['current_index'] + 1:
                        fetch_and_store_question()
                    st.rerun()
    else:
        st.info("טוען שאלה...")
        fetch_and_store_question()
        st.rerun()

else:
    st.header("הבחינה הסתיימה")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
