import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_question_to_queue

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# --- CSS מבודד לתיקון הבעיות הספציפיות ---
st.markdown("""
    <style>
    /* יישור כללי לימין */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון רדיו בשאלות: עיגול מימין ומרווח */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 20px !important;
        border: none !important;
        padding: 10px 0 !important;
    }

    /* תיקון צ'קבוקס בעמוד הסבר: מרווח וללא מסגרת */
    [data-testid="stCheckbox"] label {
        display: flex !important;
        gap: 15px !important;
        border: none !important;
        padding: 5px 0 !important;
    }
    [data-testid="stCheckbox"] { border: none !important; }

    /* צמצום רווחים בראש הדף */
    .block-container { padding-top: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    if not state['questions']:
        fetch_question_to_queue() # ייצור שאלה 1 ברקע
    
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    <div style="direction: rtl; line-height: 1.6;">
        <p>• לבחינה 25 שאלות אמריקאיות</p>
        <p>• זמן הבחינה הוא 90 דקות</p>
        <p>• ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה על השאלה הנוכחית</p>
        <p>• ניתן לנווט בין השאלות שכבר ענית עליהן</p>
        <p>• סיימת את הבחינה לחץ/י על כפתור סיים בחינה</p>
        <p>• בתום הזמן המבחן מסתיים במיידי ולא תוכל להמשיך לנווט</p>
        <p>• בסיום הבחינה תקבל משוב על הצלחתך</p>
    </div>
    """, unsafe_allow_html=True)
    
    agreed = st.checkbox("קראתי ומאשר את תנאי הבחינה")
    if st.button("התחל בחינה", disabled=not agreed):
        state['start_time'] = time.time()
        state['current_index'] = 0
        fetch_question_to_queue() # ייצור שאלה 2 ברקע
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # שעון HTML - רקע לבן, ממורכז
    timer_html = f"""
    <div style="display: flex; justify-content: center; background-color: white;">
        <div id="countdown" style="
            font-family: Arial, sans-serif;
            font-size: 48px;
            font-weight: bold;
            color: #2c3e50;
            background-color: white;
            padding: 5px 20px;
            text-align: center;
        ">00:00</div>
    </div>
    <script>
        var timeLeft = {remaining};
        function updateTimer() {{
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            document.getElementById('countdown').innerHTML = (m < 10 ? '0' : '') + m + ":" + (s < 10 ? '0' : '') + s;
            if (timeLeft > 0) {{
                timeLeft--;
                setTimeout(updateTimer, 1000);
            }} else {{
                window.parent.location.reload();
            }}
        }}
        updateTimer();
    </script>
    """
    components.html(timer_html, height=80)

    # סידבר לניווט
    with st.sidebar:
        st.write("### ניווט שאלות")
        for i in range(0, 25, 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx < 25:
                    is_loaded = idx < len(state['questions'])
                    if cols[j].button(f"{idx+1}", key=f"n_{idx}", disabled=not is_loaded):
                        state['current_index'] = idx
                        st.rerun()

    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.write(q['question_text'])
        
        current_ans = state['answers'].get(state['current_index'], None)
        # רדיו עם label_visibility="collapsed" כדי למנוע כותרת "בחר תשובה" מיותרת
        choice = st.radio("", q['options'], index=current_ans, key=f"r_{state['current_index']}", label_visibility="collapsed")
        
        if choice:
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
                can_next = state['current_index'] in state['answers']
                if st.button("⬅️ שאלה הבאה", disabled=not can_next):
                    state['current_index'] += 1
                    # Prefetch לשאלה הבאה אם היא עדיין לא בתור
                    if len(state['questions']) <= state['current_index'] + 1:
                        fetch_question_to_queue()
                    st.rerun()
    
    time.sleep(1)
    st.rerun()

else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
