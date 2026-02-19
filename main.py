import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# הזרקת CSS לפתרון RTL מלא ורדיו-באטן מימין
st.markdown("""
    <style>
    /* יישור גלובלי לימין */
    [data-testid="stAppViewContainer"], .main, .block-container, [data-testid="stSidebar"], h1, h2, h3, p, span {
        direction: rtl !important;
        text-align: right !important;
    }

    /* הגדלת גופנים */
    .question-text { font-size: 1.5rem !important; font-weight: bold; margin-bottom: 25px; }
    
    /* רדיו באטן - עיגול מימין למלל */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        font-size: 1.3rem !important;
    }
    
    /* צ'קבוקס עם רווח כפול מהמלל */
    [data-testid="stCheckbox"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 30px !important; /* רווח גדול בין הריבוע למלל */
    }

    /* הסתרת כפתורי רדיו דפולטיביים שבורים */
    [data-testid="stRadio"] div[role="radiogroup"] {
        align-items: flex-start !important;
    }

    /* ביטול ריענון ויזואלי מהיר של כפתורים */
    button { transition: none !important; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# פונקציית שעון "שקטה" ככל הניתן ב-Streamlit
@st.fragment
def show_timer():
    if state['start_time']:
        elapsed = time.time() - state['start_time']
        remaining = max(0, 300 - int(elapsed))
        st.markdown(f"## ⏳ {remaining // 60}:{remaining % 60:02d}")
        if remaining <= 0:
            state['is_finished'] = True
            st.rerun()
        time.sleep(1)
        st.rerun()

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("הוראות לבחינה")
    st.write("### ברוכים הבאים")
    st.write("לרשותך 5 שאלות ו-5 דקות לסיום הבחינה.")
    
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
            st.error("עליך לאשר את ההוראות תחילה.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    with st.sidebar:
        show_timer() # הפעלת השעון השקט
        st.divider()
        st.write("### ניווט")
        # ניווט 4 בשורה
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

    # תוכן השאלה
    q = state['questions'][state['current_index']]
    st.markdown(f"<div class='question-text'>שאלה {state['current_index'] + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-text'>{q['question_text']}</div>", unsafe_allow_html=True)
    
    ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice is not None:
        state['answers'][state['current_index']] = q['options'].index(choice)

    st.divider()
    
    # סידור כפתורים חדש: [הבא] [הגש] [הקודם]
    col_next, col_finish, col_prev = st.columns([1,1,1])
    
    with col_prev:
        if state['current_index'] > 0:
            if st.button("➡️ הקודם"):
                state['current_index'] -= 1
                st.rerun()
                
    with col_finish:
        # כפתור הגש מופיע רק בשאלה האחרונה (5)
        if state['current_index'] == 4:
            if st.button("🏁 סיים והגש בחינה", type="primary"):
                state['is_finished'] = True
                st.rerun()

    with col_next:
        if state['current_index'] < 4:
            has_ans = state['current_index'] in state['answers']
            if st.button("שאלה הבאה ⬅️", disabled=not has_ans):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

# --- עמוד סיום ---
else:
    st.title("סיכום הגשה")
    st.markdown("---")
    count = len(state['answers'])
    st.subheader(f"ענית על {count} שאלות מתוך 5.")
    st.write("הבחינה הסתיימה בהצלחה.")
    
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
