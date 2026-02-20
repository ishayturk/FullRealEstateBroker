import streamlit as st
import time
from logic import initialize_exam, fetch_next_question

st.set_page_config(page_title="סימולטור בחינה", layout="wide")

# CSS מתוקן: רדיו מימין, מלל RTL, אבל עמוד ממורכז בפריים
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; max-width: 900px; margin: auto; }
    
    /* יישור טקסט כללי לימין */
    .stMarkdown, .stSubheader, p, label, .stCheckbox {
        direction: rtl !important;
        text-align: right !important;
    }

    /* תיקון רדיו: עיגול מימין למלל */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px;
    }

    /* התאמת צ'קבוקס לימין */
    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# הפעלת מנגנון השרשרת ברקע
if state['current_index'] >= 0 and not state['is_finished']:
    fetch_next_question()

# --- עמוד הסבר עם אישור (Checkbox) ---
if state['current_index'] == -1:
    # טעינת שאלה 1 כבר עכשיו כדי שתהיה מוכנה
    if not state['questions']: fetch_next_question()
    
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    * המבחן כולל **25 שאלות** המיוצרות בזמן אמת.
    * זמן מוקצב: **90 דקות**.
    * מעבר לשאלה הבאה מתאפשר רק לאחר בחירת תשובה.
    * ניתן לנווט חזרה לשאלות קודמות דרך התפריט הצידי.
    * ציון עובר: **60**.
    """)
    
    st.divider()
    agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל בבחינה")
    
    if st.button("התחל בחינה", disabled=not agree):
        state['start_time'] = time.time()
        state['current_index'] = 0
        st.rerun()

# --- עמוד בחינה ---
elif not state['is_finished']:
    # חישוב זמן
    elapsed = int(time.time() - state['start_time'])
    remaining = max(0, 5400 - elapsed)
    mins, secs = divmod(remaining, 60)
    
    st.markdown(f"<h3 style='text-align: center; color: red;'>זמן נותר: {mins:02d}:{secs:02d}</h3>", unsafe_allow_html=True)

    # סידבר ניווט
    with st.sidebar:
        st.markdown("<h3 style='text-align: right;'>ניווט שאלות</h3>", unsafe_allow_html=True)
        for i in range(len(state['questions'])):
            status = " (V)" if i in state['answers'] else ""
            if st.button(f"שאלה {i+1}{status}", key=f"nav_{i}", use_container_width=True):
                state['current_index'] = i
                st.rerun()

    # הצגת השאלה
    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.markdown(f"**{q['question_text']}**")
        
        current_ans = state['answers'].get(state['current_index'], None)
        choice = st.radio("", q['options'], index=current_ans, key=f"q_{state['current_index']}")
        
        if choice:
            state['answers'][state['current_index']] = q['options'].index(choice)

        st.divider()
        col1, col2 = st.columns(2)
        with col2:
            if state['current_index'] > 0:
                if st.button("שאלה קודמת", use_container_width=True):
                    state['current_index'] -= 1
                    st.rerun()
        with col1:
            if state['current_index'] < 24:
                # כפתור הבא פעיל רק אם ענו ואם השאלה הבאה כבר נוצרה
                next_ready = (state['current_index'] + 1 < len(state['questions']))
                has_answered = state['current_index'] in state['answers']
                if st.button("שאלה הבאה", disabled=not (next_ready and has_answered), use_container_width=True):
                    state['current_index'] += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה", color="green", use_container_width=True):
                    state['is_finished'] = True
                    st.rerun()
    else:
        st.info("מייצר את השאלה הבאה... מיד ממשיכים.")
        time.sleep(1.5)
        st.rerun()

else:
    st.header("תוצאות הבחינה")
    st.write(f"השלמת {len(state['answers'])} מתוך 25 שאלות.")
    if st.button("התחל מחדש"):
        st.session_state.clear()
        st.rerun()
