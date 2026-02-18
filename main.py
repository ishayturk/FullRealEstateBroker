import streamlit as st
from logic import ExamManager
import time

# הגדרות יישור RTL מלאות כולל כותרות
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stApp, h1, h2, h3, p, label, div, button { direction: rtl !important; text-align: right !important; }
    div[data-testid="stSidebarNav"] { direction: rtl; }
    .stButton button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

exam = ExamManager(total_questions=10, time_limit=120)

# --- דף מעבר (Lobby) ---
if 'exam_started' not in st.session_state:
    st.title("מערכת בחינת המתווכים - C-01")
    
    # טעינת 5 ראשונות ברקע בזמן שהמשתמש בדף המעבר
    if not st.session_state.questions:
        with st.spinner("מושך 5 שאלות ראשונות מהמאגר..."):
            exam.fetch_batch(0)
    
    st.subheader("הנחיות:")
    st.write(f"בחינה מקורית מהאתר. {exam.total_questions} שאלות, {exam.time_limit} שניות.")
    
    confirm = st.checkbox("קראתי את ההנחיות ממשיך לכל הבחינה")
    if st.button("התחל בחינה", disabled=not confirm):
        st.session_state.exam_started = True
        st.session_state.start_time = time.time()
        st.session_state.current_idx = 0
        st.rerun()

# --- מסך הבחינה ---
else:
    curr = st.session_state.current_idx
    
    # טעינה מדורגת ברקע לפי הלוגיקה:
    if curr == 0 and len(st.session_state.questions) < 10:
        exam.fetch_batch(5) # טוען את 6-10 ברקע כשהמשתמש בשאלה 1
    
    # Sidebar - מספרים בלבד בגריד
    st.sidebar.title("ניווט")
    cols = st.sidebar.columns(3)
    for i in range(exam.total_questions):
        with cols[i % 3]:
            # כפתור נעול אם השאלה טרם נטענה או אם לא ענו על הקודמת
            locked = i >= len(st.session_state.questions) or (i > 0 and i-1 not in st.session_state.answers)
            if st.button(f"{i+1}", key=f"n_{i}", disabled=locked):
                st.session_state.current_idx = i
                st.rerun()

    # הצגת השאלה
    if not exam.is_time_up():
        q = st.session_state.questions[curr]
        st.subheader(f"שאלה {q['id']}")
        st.write(q['question'])
        
        ans = st.radio("בחר תשובה:", q['options'], key=f"r_{curr}", index=None)
        if ans:
            st.session_state.answers[curr] = ans
            
        if st.button("הבא", disabled=curr not in st.session_state.answers or curr == exam.total_questions-1):
            st.session_state.current_idx += 1
            st.rerun()
    else:
        st.error("הזמן נגמר!")
