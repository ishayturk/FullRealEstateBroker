import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# CSS לשיפור הממשק בלבד - ללא שינוי לוגיקה
st.markdown("""
    <style>
    /* יישור RTL גלובלי */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* תיקון נקודת הרדיו שתהיה מימין למלל */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        display: flex !important;
    }
    
    /* עיצוב השעון במרכז */
    .timer-container {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        color: #ff4b4b;
        background-color: rgba(255, 75, 75, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #ff4b4b;
        margin: 20px auto;
        width: fit-content;
        min-width: 220px;
    }

    /* שיפור כפתורים */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("הוראות לבחינה")
    st.write("מבחן תרגול - 5 שאלות בנושאי אתיקה ותיווך.")
    
    if st.button("התחל בחינה"):
        state['questions'] = [generate_question_sync(0)]
        state['current_index'] = 0
        state['start_time'] = time.time()
        st.rerun()

# --- עמוד בחינה ---
elif not state['is_finished']:
    elapsed = time.time() - state['start_time']
    remaining = max(0, 300 - int(elapsed))
    
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # תצוגת שעון במרכז (לא בסידבר)
    st.markdown(f"<div class='timer-container'>⏳ {remaining // 60}:{remaining % 60:02d}</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.write("### ניווט")
        for i in range(5):
            if st.button(f"שאלה {i+1}", key=f"nav_{i}", type="primary" if i == state['current_index'] else "secondary"):
                while len(state['questions']) <= i:
                    state['questions'].append(generate_question_sync(len(state['questions'])))
                state['current_index'] = i
                st.rerun()

    q = state['questions'][state['current_index']]
    st.subheader(f"שאלה {state['current_index'] + 1}")
    st.write(f"### {q['question_text']}")
    
    ans = state['answers'].get(state['current_index'], None)
    # הרדיו עכשיו מיושר לימין בזכות ה-CSS
    choice = st.radio("בחר תשובה:", q['options'], index=ans, key=f"q_{state['current_index']}")
    
    if choice:
        state['answers'][state['current_index']] = q['options'].index(choice)

    st.divider()
    col1, col_finish, col2 = st.columns([1, 1, 1])
    
    with col1:
        if state['current_index'] < 4:
            if st.button("⬅️ שאלה הבאה"):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()
    
    with col_finish:
        if state['current_index'] == 4:
            if st.button("🏁 סיום בחינה", type="primary"):
                state['is_finished'] = True
                st.rerun()
                
    with col2:
        if state['current_index'] > 0:
            if st.button("שאלה קודמת ➡️"):
                state['current_index'] -= 1
                st.rerun()

    # רענון שקט לעדכון השעון
    time.sleep(1)
    st.rerun()

# --- עמוד סיום ---
else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
