import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="sidebar-close"] { display: none !important; }
    
    .instruction-box {
        direction: rtl;
        text-align: right;
        padding-right: 20px;
    }

    /* עיצוב הרדיו - הפרדה מהמלל והצמדה לימין */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 25px !important; /* מרווח מוגדל בין העיגול למלל */
        padding: 10px 0;
    }

    /* צ'קבוקס עם מסגרת שחורה דקה */
    [data-testid="stCheckbox"] {
        border: 1px solid #000;
        padding: 10px;
        border-radius: 4px;
        width: fit-content;
    }

    /* כפתורים שקופים */
    .stButton>button {
        background-color: transparent !important;
        border: 1px solid #333 !important;
        color: #333 !important;
    }

    /* שעון ללא רקע */
    .timer-container {
        text-align: center;
        font-family: sans-serif;
        font-size: 40px;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

if state['current_index'] == -1:
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    <div class="instruction-box">
        <ul>
            <li>לבחינה 25 שאלות אמריקאיות</li>
            <li>זמן הבחינה הוא 90 דקות</li>
            <li>ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה על השאלה הנוכחית</li>
            <li>ניתן לנווט בין השאלות שכבר ענית עליהן</li>
            <li>סיימת את הבחינה לחץ/י על כפתור סיים בחינה</li>
            <li>בתום הזמן המבחן מסתיים במיידי ולא תוכל להמשיך לנווט ולענות על שאלות</li>
            <li>בסיום הבחינה יזום או בשל הזמן תקבל משוב על הבחינה</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    agreed = st.checkbox("קראתי ומאשר")
    if st.button("התחל בחינה", disabled=not agreed):
        state['questions'] = [generate_question_sync(0)]
        state['current_index'] = 0
        state['start_time'] = time.time()
        st.rerun()

elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # רכיב שעון ללא רקע
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
        st.write("### ניווט שאלות")
        for i in range(0, 25, 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx < 25:
                    can_nav = idx < len(state['questions'])
                    if cols[j].button(f"{idx+1}", key=f"n_{idx}", disabled=not can_nav):
                        state['current_index'] = idx
                        st.rerun()

    q = state['questions'][state['current_index']]
    st.subheader(f"שאלה {state['current_index'] + 1}")
    st.markdown(f"#### {q['question_text']}")
    
    ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice is not None:
        state['answers'][state['current_index']] = q['options'].index(choice)

    st.divider()
    c1, c2, c3 = st.columns([1,1,1])
    with c3:
        if state['current_index'] > 0:
            if st.button("שאלה קודמת ➡️"):
                state['current_index'] -= 1
                st.rerun()
    with c2:
        if state['current_index'] == 24 or len(state['answers']) >= 25:
            if st.button("🏁 סיים בחינה"):
                state['is_finished'] = True
                st.rerun()
    with c1:
        if state['current_index'] < 24:
            has_ans = state['current_index'] in state['answers']
            if st.button("⬅️ שאלה הבאה", disabled=not has_ans):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    time.sleep(1)
    st.rerun()

else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
