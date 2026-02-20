import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide", initial_sidebar_state="expanded")

# CSS לפתרון בעיות ויזואליות: יישור, רדיו, צ'קבוקס ומניעת ריצוד
st.markdown("""
    <style>
    /* יישור RTL גלובלי */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* מניעת סגירת סידבר */
    [data-testid="sidebar-close"] { display: none !important; }
    
    /* יישור בולטים - הצמדת המלל לנקודה */
    .instruction-box {
        direction: rtl;
        text-align: right;
        padding-right: 20px;
    }

    /* רדיו באטן - נקודה מימין עם מרווח ומסגרת */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 15px !important;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
    }

    /* צ'קבוקס עם מסגרת בולטת */
    [data-testid="stCheckbox"] {
        border: 2px solid #333;
        padding: 15px;
        border-radius: 10px;
        width: fit-content;
        margin: 20px 0;
    }

    /* כפתורים שקופים ומקצועיים */
    .stButton>button {
        background-color: transparent !important;
        border: 1px solid #333 !important;
        color: #333 !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר לבחינה ---
if state['current_index'] == -1:
    st.title("הסבר לבחינת רישיון למתווכים")
    
    # שימוש ב-HTML ליישור בולטים מושלם
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
    
    st.divider()
    agreed = st.checkbox("קראתי ומאשר")
    
    if st.button("התחל בחינה", disabled=not agreed):
        state['questions'] = [generate_question_sync(0)]
        state['current_index'] = 0
        state['start_time'] = time.time()
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # שעון JavaScript שקט - לא מרעיד את התפריט
    total_seconds = 5400
    elapsed = int(time.time() - state['start_time'])
    remaining = max(0, total_seconds - elapsed)
    
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # רכיב שעון "חי" שלא מצריך rerun של כל הדף
    timer_html = f"""
    <div style="text-align:center; font-family:sans-serif; font-size:40px; font-weight:bold; padding:10px; background:#f0f2f6; border-radius:10px; border:1px solid #ccc;">
        <span id="timer"></span>
    </div>
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
    components.html(timer_html, height=100)

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

# --- עמוד סיום ---
else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות מתוך 25.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
