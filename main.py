import streamlit as st
from logic import ExamManager

# הגדרות דף ויישור RTL מלא כולל כותרות
st.set_page_config(page_title="בחינת מתווכים C-01", layout="wide")
st.markdown("""
    <style>
    /* יישור כל האפליקציה לימין */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* תיקון ספציפי לכותרות (h1, h2, h3) */
    h1, h2, h3, h4, p, span, label {
        direction: rtl !important;
        text-align: right !important;
    }
    /* הצמדת רכיבי טפסים לימין */
    div[data-testid="stCheckbox"], div[data-testid="stRadio"] {
        direction: rtl;
        text-align: right;
    }
    /* סידבר */
    section[data-testid="stSidebar"] {
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

exam = ExamManager(total_questions=10, time_limit=120)

# --- דף מעבר (Lobby) ---
if 'exam_started' not in st.session_state:
    st.title("מערכת בחינת מתווכים") # כעת יהיה בימין
    st.subheader("הנחיות לבחינה:")
    st.write("1. בחינה זו כוללת 10 שאלות.")
    st.write("2. לרשותך 120 שניות בדיוק.")
    
    # טעינת 5 ראשונות ברקע (בלובי)
    if not st.session_state.questions:
        exam.fetch_questions_batch(0)
    
    confirm = st.checkbox("קראתי את ההנחיות ממשיך לכל הבחינה")
    if st.button("התחל בחינה", disabled=not confirm):
        exam.start_exam()
        st.rerun()

# --- מהלך הבחינה ---
else:
    curr = st.session_state.current_idx
    # טעינת 5 הבאות ברקע כשהמשתמש בשאלה הראשונה
    if curr == 0 and len(st.session_state.questions) < 10:
        exam.fetch_questions_batch(5)
    
    # Sidebar - גריד מספרים
    st.sidebar.title("ניווט בשאלות")
    cols = st.sidebar.columns(3)
    for i in range(exam.total_questions):
        col_idx = i % 3
        # חסימת כפתור אם השאלה טרם נטענה או אם לא ענו על הקודמת
        is_disabled = i > len(st.session_state.questions) - 1 or (i > 0 and (i-1) not in st.session_state.answers)
        if cols[col_idx].button(f"{i+1}", key=f"btn_{i}", disabled=is_disabled):
            st.session_state.current_idx = i
            st.rerun()

    # הצגת השאלה (לא ריקה)
    if curr < len(st.session_state.questions):
        q = st.session_state.questions[curr]
        st.subheader(f"שאלה {q['id']}")
        st.write(q['question'])
        
        choice = st.radio("בחר את התשובה הנכונה:", q['options'], key=f"q_{curr}", index=None)
        
        if choice:
            st.session_state.answers[curr] = choice

        col_prev, col_next = st.columns(2)
        if curr > 0:
            if col_prev.button("הקודם"):
                st.session_state.current_idx -= 1
                st.rerun()
        
        if curr < exam.total_questions - 1:
            if col_next.button("הבא", disabled=curr not in st.session_state.answers):
                st.session_state.current_idx += 1
                st.rerun()
        else:
            if st.button("סיים בחינה"):
                st.success("הבחינה הסתיימה בהצלחה!")
