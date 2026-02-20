import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_next_question

st.set_page_config(page_title="סימולטור בחינה", layout="wide")

# CSS RTL אגרסיבי מותאם ל-Iframe ולרדיו
st.markdown("""
    <style>
    /* ביטול שוליים לעבודה בתוך פריים */
    .block-container { padding: 1rem !important; max-width: 100% !important; }
    
    /* יישור כללי לימין */
    .stApp, [data-testid="stSidebar"], [data-testid="stMarkdownContainer"] {
        direction: rtl !important;
        text-align: right !important;
    }

    /* תיקון רדיו - העיגול מימין למלל (כמו באפליקציית הלימוד) */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 10px;
    }

    /* יישור כותרות וטקסט */
    h1, h2, h3, .stSubheader, p, label {
        text-align: right !important;
        direction: rtl !important;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# הפעלת מנגנון השרשרת ברקע בכל הרצה
if state['current_index'] >= 0 and not state['is_finished']:
    fetch_next_question()

# --- עמוד הסבר ---
if state['current_index'] == -1:
    # טעינת השאלה הראשונה מראש
    if not state['questions']: fetch_next_question()
    
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    1. המבחן כולל 25 שאלות.
    2. זמן מוקצב: 90 דקות.
    3. מעבר לשאלה הבאה רק לאחר סימון תשובה.
    4. ניתן לחזור אחורה רק לשאלות שנענו.
    5. בסיום 90 דקות המבחן יינעל.
    6. ציון עובר: 60.
    7. חל איסור על שימוש בחומר עזר.
    """)
    
    if st.button("התחל בחינה"):
        state['start_time'] = time.time()
        state['current_index'] = 0
        st.rerun()

# --- עמוד בחינה ---
elif not state['is_finished']:
    elapsed = int(time.time() - state['start_time'])
    remaining = max(0, 5400 - elapsed)
    
    # טיימר מינימליסטי
    st.markdown(f"<h3 style='text-align: center;'>זמן נותר: {remaining // 60:02d}:{remaining % 60:02d}</h3>", unsafe_allow_html=True)

    with st.sidebar:
        st.write("### ניווט")
        for i in range(len(state['questions'])):
            label = f"שאלה {i+1}" + (" (V)" if i in state['answers'] else "")
            if st.button(label, key=f"nav_{i}"):
                state['current_index'] = i
                st.rerun()

    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.write(q['question_text'])
        
        ans_idx = state['answers'].get(state['current_index'], None)
        choice = st.radio("", q['options'], index=ans_idx, key=f"q_{state['current_index']}", label_visibility="collapsed")
        
        if choice is not None:
            state['answers'][state['current_index']] = q['options'].index(choice)

        st.divider()
        col1, col2 = st.columns(2)
        with col2:
            if state['current_index'] > 0:
                if st.button("שאלה קודמת"):
                    state['current_index'] -= 1
                    st.rerun()
        with col1:
            if state['current_index'] < 24:
                btn_label = "שאלה הבאה"
                is_disabled = state['current_index'] not in state['answers'] or (state['current_index'] + 1 >= len(state['questions']))
                if st.button(btn_label, disabled=is_disabled):
                    state['current_index'] += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה"):
                    state['is_finished'] = True
                    st.rerun()
    else:
        st.info("מייצר את השאלה הבאה... המתן רגע.")
        time.sleep(1)
        st.rerun()

else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} מתוך 25 שאלות.")
    if st.button("התחל מחדש"):
        st.session_state.clear()
        st.rerun()
