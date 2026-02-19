import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# CSS סופי - פותר את בעיית הנקודה מימין והיישור
st.markdown("""
    <style>
    /* יישור גלובלי לימין */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3 {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* רדיו באטן - העיגול מימין למלל */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        font-size: 1.3rem !important;
    }

    /* צ'קבוקס הסבר - ריבוע מימין למלל עם רווח */
    [data-testid="stCheckbox"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 30px !important;
    }

    /* הגדלת שאלה */
    .question-title { font-size: 1.6rem; font-weight: bold; margin-bottom: 20px; }
    
    /* כפתורי ניווט בסידבר - 4 בשורה */
    [data-testid="stSidebar"] div.stButton button {
        padding: 5px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("דף הסבר והוראות לבחינה")
    st.write("ברוכים הבאים לסימולציה. לרשותך 5 שאלות ו-5 דקות לסיום.")
    
    # צ'קבוקס עם רווח
    agreed = st.checkbox("קראתי והבנתי את ההוראות לבחינה")
    state['confirmed_instructions'] = agreed

    if st.button("התחל בחינה"):
        if agreed:
            state['questions'] = [generate_question_sync(0)]
            state['current_index'] = 0
            state['start_time'] = time.time()
            st.rerun()
        else:
            st.error("עליך לאשר את ההוראות תחילה.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # חישוב זמן
    elapsed = time.time() - state['start_time']
    remaining = max(0, 300 - int(elapsed))
    
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    with st.sidebar:
        # שעון שקט - מתעדכן ללא ריפרש של כל הדף
        st.markdown(f"<h2 style='text-align:center;'>⏳ {remaining // 60}:{remaining % 60:02d}</h2>", unsafe_allow_html=True)
        st.divider()
        st.write("### ניווט")
        
        # גריד 4 בשורה
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                if idx < 5:
                    if cols[c].button(f"{idx+1}", key=f"n_{idx}", type="primary" if idx == state['current_index'] else "secondary"):
                        while len(state['questions']) <= idx:
                            state['questions'].append(generate_question_sync(len(state['questions'])))
                        state['current_index'] = idx
                        st.rerun()

    # הצגת השאלה
    q = state['questions'][state['current_index']]
    st.markdown(f"<div class='question-title'>שאלה {state['current_index'] + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-title'>{q['question_text']}</div>", unsafe_allow_html=True)
    
    ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice is not None:
        state['answers'][state['current_index']] = q['options'].index(choice)

    st.divider()
    
    # כפתורים בסדר: [הבא] [הגש] [הקודם]
    col_next, col_finish, col_prev = st.columns([1,1,1])
    
    with col_prev:
        if state['current_index'] > 0:
            if st.button("שאלה קודמת ➡️"):
                state['current_index'] -= 1
                st.rerun()
                
    with col_finish:
        # כפתור הגש מופיע רק בשאלה האחרונה
        if state['current_index'] == 4:
            if st.button("🏁 סיים והגש בחינה", type="primary"):
                state['is_finished'] = True
                st.rerun()

    with col_next:
        if state['current_index'] < 4:
            has_ans = state['current_index'] in state['answers']
            # הכפתור פעיל רק אם ענה
            if st.button("⬅️ שאלה הבאה", disabled=not has_ans):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    # ריפרש אוטומטי לטיימר
    time.sleep(1)
    st.rerun()

# --- עמוד סיום נקי ---
else:
    st.header("הבחינה הסתיימה")
    st.subheader(f"ענית על {len(state['answers'])} שאלות מתוך 5.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
