import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

# הגדרות עיצוב RTL קשיחות
st.set_page_config(page_title="סימולטור רשם המתווכים", layout="centered")

st.markdown("""
    <style>
    /* יישור כללי לימין */
    .main .block-container, .stMarkdown, .stRadio, .stButton, .stCheckbox, [data-testid="stSidebar"] {
        direction: rtl !important;
        text-align: right !important;
    }
    /* תיקון כפתורי רדיו - עיגול מימין לטקסט */
    .stRadio div[role="radiogroup"] {
        flex-direction: column;
    }
    .stRadio label {
        display: flex;
        flex-direction: row-reverse;
        justify-content: flex-end;
        gap: 10px;
    }
    /* הקטנת גופנים */
    .question-text { font-size: 1rem !important; font-weight: bold; }
    p, label { font-size: 0.9rem !important; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("הוראות לבחינה")
    st.markdown("### ברוכים הבאים למבחן האתיקה")
    st.write("מבחן זה מדמה את שאלות רשם המתווכים. לרשותך 5 שאלות ו-5 דקות.")
    
    agreed = st.checkbox("קראתי והבנתי את ההוראות לבחינה", value=state['confirmed_instructions'])
    state['confirmed_instructions'] = agreed

    if st.button("התחל בחינה"):
        if agreed:
            # ייצור שאלה ראשונה במידה והרשימה ריקה
            if not state['questions']:
                state['questions'].append(generate_question_sync(0))
            state['current_index'] = 0
            state['start_time'] = time.time()
            st.rerun()
        else:
            st.warning("חובה לאשר את ההוראות.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # טיימר בסידבר - שימוש ב-empty כדי שיתרפרש
    with st.sidebar:
        timer_placeholder = st.empty()
        elapsed = time.time() - state['start_time']
        remaining = max(0, 300 - int(elapsed))
        timer_placeholder.markdown(f"### ⏳ זמן נותר: {remaining // 60}:{remaining % 60:02d}")
        
        st.divider()
        st.write("### ניווט שאלות")
        # לוגיקת ניווט: כפתור לכל שאלה
        cols = st.columns(3)
        for i in range(5):
            btn_label = f"שאלה {i+1}"
            # הדגשת השאלה הנוכחית
            if i == state['current_index']:
                btn_label = f"📍 {i+1}"
            
            if cols[i % 3].button(btn_label, key=f"nav_{i}"):
                # אם עוברים לשאלה שעוד לא נוצרה - מייצרים אותה
                while len(state['questions']) <= i:
                    state['questions'].append(generate_question_sync(len(state['questions'])))
                state['current_index'] = i
                st.rerun()

    # גוף השאלה
    q_data = state['questions'][state['current_index']]
    st.markdown(f"<div class='question-text'>שאלה {state['current_index'] + 1} מתוך 5</div>", unsafe_allow_html=True)
    st.write(q_data['question_text'])
    
    # בחירת תשובה - אינדקס None כדי שלא תהיה בחורה מראש
    current_ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("בחר את התשובה הנכונה:", q_data['options'], index=current_ans, key=f"q_{state['current_index']}")
    
    if choice:
        state['answers'][state['current_index']] = q_data['options'].index(choice)

    # כפתורי ניווט תחתונים
    st.divider()
    col_prev, col_finish, col_next = st.columns([1,1,1])
    
    with col_prev:
        if state['current_index'] > 0:
            if st.button("⬅️ הקודם"):
                state['current_index'] -= 1
                st.rerun()
    
    with col_finish:
        if st.button("🏁 הגש מבחן"):
            state['is_finished'] = True
            st.rerun()

    with col_next:
        if state['current_index'] < 4:
            if st.button("הבא ➡️"):
                state['current_index'] += 1
                # טעינה מראש של השאלה הבאה אם צריך
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    # ריפרש אוטומטי קל לטיימר
    if remaining > 0:
        time.sleep(1)
        st.rerun()

# --- עמוד סיום ---
else:
    st.title("סיכום מבחן")
    st.write(f"ענית על {len(state['answers'])} שאלות מתוך 5.")
    if st.button("התחל מבחן חדש"):
        st.session_state.clear()
        st.rerun()
