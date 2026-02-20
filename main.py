import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide", initial_sidebar_state="expanded")

# CSS לתיקון יישור, רדיו וצ'קבוקס
st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* יישור רשימת ההסבר - מניעת בריחת מלל לשמאל */
    .stMarkdown ul { list-style-position: inside; padding-right: 0; }
    
    /* רדיו באטן - נקודה מימין למלל */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        display: flex !important;
        gap: 10px;
    }

    /* מסגרת שחורה לצ'קבוקס */
    [data-testid="stCheckbox"] {
        border: 1px solid black;
        padding: 10px;
        border-radius: 5px;
        width: fit-content;
    }

    /* שעון שקט במרכז */
    .timer-display {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        color: #333;
    }

    /* כפתורים שקופים */
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
    st.markdown("""
    * לבחינה 25 שאלות אמריקאיות
    * זמן הבחינה הוא 90 דקות
    * ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה על השאלה הנוכחית
    * ניתן לנווט בין השאלות שכבר ענית עליהן
    * סיימת את הבחינה לחץ/י על כפתור סיים בחינה
    * בתום הזמן המבחן מסתיים במיידי ולא תוכל להמשיך לנווט ולענות על שאלות
    * בסיום הבחינה יזום או בשל הזמן תקבל משוב על הבחינה
    """)
    
    agreed = st.checkbox("קראתי ומאשר")
    if st.button("התחל בחינה", disabled=not agreed):
        state['questions'] = [generate_question_sync(0)]
        state['current_index'] = 0
        state['start_time'] = time.time()
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # שעון ללא איקונים
    st.markdown(f"<div class='timer-display'>{remaining // 60:02d}:{remaining % 60:02d}</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.write("### ניווט")
        # 4 בשורה
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
    st.write(q['question_text'])
    
    ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    if choice: state['answers'][state['current_index']] = q['options'].index(choice)

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
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    time.sleep(1)
    st.rerun()

# --- עמוד סיום ---
else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
