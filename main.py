import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# CSS אגרסיבי לתיקון RTL ורדיו באטן
st.markdown("""
    <style>
    /* יישור כללי לימין לכל המכולות */
    [data-testid="stAppViewContainer"], .main, .block-container, [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* יישור כותרות וטקסט בדף ההסבר */
    h1, h2, h3, p, span, .stMarkdown {
        direction: rtl !important;
        text-align: right !important;
        width: 100%;
    }

    /* הגדלת גופנים */
    .question-text { font-size: 1.5rem !important; font-weight: bold; margin-bottom: 20px; }
    .stRadio label { font-size: 1.3rem !important; }

    /* תיקון רדיו באטן - נקודה מימין לטקסט */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px;
    }
    
    /* עיצוב כפתורי ניווט בסידבר - 4 בשורה */
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        gap: 5px !important;
    }
    
    /* הסתרת כפתור "הבא" אם לא נבחרה תשובה (אופציונלי דרך לוגיקה) */
    
    /* ביטול צבע אדום לכפתורים */
    button {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# משתנה גלובלי למניעת שגיאת NameError בסוף
remaining = 300 

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("הוראות לבחינה")
    st.markdown("### קרא בעיון את ההנחיות")
    st.write("מבחן זה כולל 5 שאלות. עליך לאשר את ההבנה בטרם תתחיל.")
    
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
            st.error("יש לאשר את ההוראות.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # חישוב זמן
    elapsed = time.time() - state['start_time']
    remaining = max(0, 300 - int(elapsed))
    
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # Sidebar
    with st.sidebar:
        # טיימר שקט (ללא רענון דף מלא)
        timer_placeholder = st.empty()
        timer_placeholder.markdown(f"## ⏳ {remaining // 60}:{remaining % 60:02d}")
        
        st.divider()
        st.write("### ניווט (4 בשורה)")
        
        # בניית גריד ניווט של 4 בשורה
        for row in range(2): # מספיק ל-5 שאלות
            cols = st.columns(4)
            for col_idx in range(4):
                q_idx = row * 4 + col_idx
                if q_idx < 5:
                    label = f"{q_idx + 1}"
                    is_current = (q_idx == state['current_index'])
                    if cols[col_idx].button(label, key=f"nav_{q_idx}", type="primary" if is_current else "secondary"):
                        while len(state['questions']) <= q_idx:
                            state['questions'].append(generate_question_sync(len(state['questions'])))
                        state['current_index'] = q_idx
                        st.rerun()

    # תצוגת שאלה
    q_data = state['questions'][state['current_index']]
    st.markdown(f"<div class='question-text'>שאלה {state['current_index'] + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-text'>{q_data['question_text']}</div>", unsafe_allow_html=True)
    
    # בחירת תשובה
    current_ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("בחר תשובה:", q_data['options'], index=current_ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice is not None:
        state['answers'][state['current_index']] = q_data['options'].index(choice)

    # כפתורי ניווט
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if state['current_index'] > 0:
            if st.button("⬅️ הקודם"):
                state['current_index'] -= 1
                st.rerun()
    
    with col2:
        if st.button("🏁 הגש מבחן"):
            state['is_finished'] = True
            st.rerun()

    with col3:
        # חסימת כפתור "הבא" אם לא נבחרה תשובה
        has_answered = state['current_index'] in state['answers']
        if state['current_index'] < 4:
            if st.button("הבא ➡️", disabled=not has_answered):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    # ריפרש של הטיימר בלבד (כדי למנוע קפיצות, זמן הריענון קטן)
    time.sleep(1)
    st.rerun()

# --- עמוד סיום ---
else:
    st.title("הבחינה הסתיימה")
    if remaining <= 0:
        st.warning("הזמן תם!")
    
    st.write(f"ענית על {len(state['answers'])} מתוך 5 שאלות.")
    
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
