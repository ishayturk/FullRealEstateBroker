import streamlit as st
import time  # התיקון לשגיאה שקיבלת
from logic import initialize_exam, get_ethics_prompt

# הגדרות תצוגה RTL מוקטנת
st.set_page_config(page_title="סימולטור רשם המתווכים", layout="centered")
st.markdown("""
    <style>
    direction: rtl; text-align: right;
    .stMarkdown, .stText, .stButton, .stCheckbox { direction: rtl; text-align: right; }
    .question-text { font-size: 1rem; font-weight: bold; }
    .stRadio > label { font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("הוראות לבחינה")
    st.write("מבחן סימולציה באתיקה למתווכים. 5 שאלות, 5 דקות.")
    
    # צ'ק בוקס חובה
    agreed = st.checkbox("קראתי והבנתי את ההוראות לבחינה")
    state['confirmed_instructions'] = agreed

    if st.button("התחל בחינה"):
        if agreed:
            state['current_index'] = 0
            state['start_time'] = time.time()
            # כאן המערכת מציגה את השאלה הראשונה שיוצרה ברקע
            st.rerun()
        else:
            st.error("עליך לאשר את קריאת ההוראות כדי להתחיל.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # טיימר
    elapsed = time.time() - state['start_time']
    remaining = max(0, 300 - int(elapsed))
    
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # סיידבר / תפריט עליון בנייד
    with st.sidebar:
        st.write(f"⏳ זמן נותר: {remaining // 60}:{remaining % 60:02d}")
        st.write(f"שאלה: {state['current_index'] + 1} / 5")
        if st.button("הגש מבחן"):
            state['is_finished'] = True
            st.rerun()

    # הצגת שאלה (כאן המערכת שולפת מהרשימה הדינמית)
    st.subheader(f"שאלה {state['current_index'] + 1}")
    
    # במידה וזו שאלה חדשה, המערכת תייצר ברקע את השאלה הבאה
    # לוגיקה: if state['current_index'] == len(state['questions']): generate...

    # כפתורי ניווט
    col1, col2 = st.columns(2)
    with col1:
        if state['current_index'] > 0:
            if st.button("הקודם"):
                state['current_index'] -= 1
                st.rerun()
    with col2:
        label = "סיים" if state['current_index'] == 4 else "הבא"
        if st.button(label):
            # כאן קורה הקסם: אם עוברים לחדשה - מייצרים ברקע את זו שאחריה
            if state['current_index'] < 4:
                state['current_index'] += 1
                st.rerun()
            else:
                state['is_finished'] = True
                st.rerun()

# --- עמוד משוב ---
else:
    st.title("סוף המבחן")
    st.write("תודה שהשתתפת.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
