import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

# הגדרות עמוד
st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# הזרקת CSS אגרסיבית לתיקון RTL, רדיו באטן וגופנים
st.markdown("""
    <style>
    /* יישור גלובלי לימין */
    .main, .stApp, [data-testid="stSidebar"], .stMarkdown, .stRadio, .stButton, .stCheckbox {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* הגדלת גופנים לשאלה ולתשובות */
    .question-text {
        font-size: 1.4rem !important;
        font-weight: bold;
        color: #1E1E1E;
        margin-bottom: 1.5rem;
    }
    
    /* תיקון כפתורי רדיו - עיגול מימין לטקסט */
    [data-testid="stRadio"] div[role="radiogroup"] {
        flex-direction: column;
    }
    [data-testid="stRadio"] label {
        display: flex;
        flex-direction: row-reverse; /* הופך את הסדר: קודם נקודה אז טקסט */
        justify-content: flex-end;
        font-size: 1.2rem !important; /* הגדלת טקסט התשובות */
        padding: 10px;
        gap: 15px;
    }
    
    /* יישור עמוד ההסבר */
    [data-testid="stVerticalBlock"] {
        align-items: flex-start;
    }

    /* תיקון צ'קבוקס הסבר */
    .stCheckbox label {
        flex-direction: row-reverse;
        justify-content: flex-end;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("דף הסבר והוראות לבחינה")
    st.write("### שים לב להנחיות הבאות:")
    st.write("1. הבחינה כוללת 5 שאלות בנושאי אתיקה וחוק המתווכים.")
    st.write("2. לרשותך 5 דקות בדיוק.")
    st.write("3. עליך לסמן את התשובה הנכונה ביותר.")
    
    # וידוא יישור לימין של הצ'קבוקס
    agreed = st.checkbox("קראתי והבנתי את ההוראות לבחינה", value=state['confirmed_instructions'])
    state['confirmed_instructions'] = agreed

    if st.button("התחל בחינה"):
        if agreed:
            if not state['questions']:
                state['questions'].append(generate_question_sync(0))
            state['current_index'] = 0
            state['start_time'] = time.time()
            st.rerun()
        else:
            st.error("חובה לסמן שקראת את ההוראות.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # חישוב זמן
    elapsed = time.time() - state['start_time']
    remaining = max(0, 300 - int(elapsed))
    
    # בדיקה אם הזמן נגמר - העברה אוטומטית
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # Sidebar: ניווט וטיימר
    with st.sidebar:
        st.markdown(f"### ⏳ זמן נותר: {remaining // 60}:{remaining % 60:02d}")
        st.divider()
        st.write("### ניווט בין שאלות")
        
        # גריד כפתורי ניווט
        for i in range(5):
            btn_type = "primary" if i == state['current_index'] else "secondary"
            if st.button(f"שאלה {i+1}", key=f"nav_{i}", use_container_width=True, type=btn_type):
                while len(state['questions']) <= i:
                    state['questions'].append(generate_question_sync(len(state['questions'])))
                state['current_index'] = i
                st.rerun()

    # הצגת השאלה במרכז
    q_data = state['questions'][state['current_index']]
    
    st.markdown(f"<div class='question-text'>שאלה {state['current_index'] + 1}:</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-text'>{q_data['question_text']}</div>", unsafe_allow_html=True)
    
    # רדיו באטן מוגדל ומיושר
    current_ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q_data['options'], index=current_ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice:
        state['answers'][state['current_index']] = q_data['options'].index(choice)

    # כפתורי ניווט תחתונים
    st.divider()
    col_prev, col_finish, col_next = st.columns([1, 1, 1])
    
    with col_prev:
        if state['current_index'] > 0:
            if st.button("⬅️ שאלה קודמת"):
                state['current_index'] -= 1
                st.rerun()
    
    with col_finish:
        # כפתור הגש מופיע רק במהלך הבחינה למטה
        if st.button("🏁 סיים והגש בחינה", type="primary"):
            state['is_finished'] = True
            st.rerun()

    with col_next:
        if state['current_index'] < 4:
            if st.button("שאלה הבאה ➡️"):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    # ריפרש אוטומטי לטיימר
    time.sleep(1)
    st.rerun()

# --- עמוד סיום ---
else:
    st.title("הבחינה הסתיימה")
    if remaining <= 0:
        st.error("הזמן הקצוב הסתיים!")
    
    st.write(f"השלמת {len(state['answers'])} שאלות מתוך 5.")
    
    if st.button("חזרה לתפריט ראשי"):
        st.session_state.clear()
        st.rerun()
