import streamlit as st
from logic import ExamManager

# הגדרות דף ויישור RTL
st.set_page_config(page_title="בחינת מתווכים C-01", layout="wide")
st.markdown("""
    <style>
    .reportview-container, .main, .stApp { direction: rtl; text-align: right; }
    div[data-testid="stSidebarNav"] { direction: rtl; }
    .stButton button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

exam = ExamManager(total_questions=10, time_limit=120)

# --- דף מעבר (Lobby) ---
if 'exam_started' not in st.session_state:
    st.title("ברוכים הבאים לבחינת המתווכים")
    st.subheader("הנחיות:")
    st.write("בחינה זו כוללת 10 שאלות. לרשותך 120 שניות.")
    
    # טעינת 5 ראשונות ברקע כבר עכשיו
    if not st.session_state.questions:
        exam.fetch_questions_batch(0)
    
    confirm = st.checkbox("קראתי את ההנחיות ממשיך לכל הבחינה")
    if st.button("התחל בחינה", disabled=not confirm):
        exam.start_exam()
        st.rerun()

# --- מהלך הבחינה ---
else:
    # טעינה מדורגת ברקע
    curr = st.session_state.current_idx
    if curr == 0 and len(st.session_state.questions) < 10:
        exam.fetch_questions_batch(5) # טוען 6-10 כשהוא בשאלה 1
    
    # Sidebar - גריד של מספרים
    st.sidebar.title("ניווט")
    cols = st.sidebar.columns(3)
    for i in range(exam.total_questions):
        col_idx = i % 3
        is_disabled = i > len(st.session_state.questions) - 1 or (i > 0 and i-1 not in st.session_state.answers)
        if cols[col_idx].button(f"{i+1}", key=f"btn_{i}", disabled=is_disabled):
            st.session_state.current_idx = i
            st.rerun()

    # תצוגת שאלה
    if not exam.is_time_up():
        q = st.session_state.questions[curr]
        st.subheader(f"שאלה {q['id']}")
        st.write(q['question'])
        
        choice = st.radio("בחר תשובה:", q['options'], key=f"q_{curr}", index=None)
        
        if choice:
            st.session_state.answers[curr] = choice

        col_prev, col_next = st.columns(2)
        if curr > 0:
            if col_prev.button("הקודם"):
                st.session_state.current_idx -= 1
                st.rerun()
        
        if curr < len(st.session_state.questions) - 1:
            if col_next.button("הבא", disabled=curr not in st.session_state.answers):
                st.session_state.current_idx += 1
                st.rerun()
        else:
            if st.button("סיים בחינה", type="primary"):
                st.session_state.time_up = True
                st.rerun()
    else:
        st.error("הזמן נגמר!")
        st.write(f"הציון שלך: {len([i for i, a in st.session_state.answers.items() if a == st.session_state.questions[i]['correct']]) * 10}")
