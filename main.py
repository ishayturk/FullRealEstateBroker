import streamlit as st
from logic import ExamManager
import time

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

st.set_page_config(page_title="מבחן רישוי למתווכים", layout="wide")

# תיקון יישור לימין (RTL) ללא רקע מיותר
st.markdown("""
    <style>
    /* הגדרת כיוון כללית */
    .stApp { direction: rtl; text-align: right; }
    /* יישור כותרות וטקסט */
    h1, h2, h3, h4, p, span, li { text-align: right !important; direction: rtl !important; }
    /* יישור רכיבי בחירה */
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    /* עיצוב כפתור */
    .stButton button { width: 100%; height: 3em; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

exam = ExamManager()

if 'exam_started' not in st.session_state:
    st.title("מבחן רישוי למתווכים במקרקעין")
    
    if exam.load_exam_from_json():
        # דברי הסבר למשתמש - מה שבאמת מעניין אותו
        st.markdown("""
        ### הנחיות לבחינה:
        * **מספר שאלות:** 25 שאלות רב-ברירה.
        * **זמן מוקצב:** 120 דקות (שעתיים). הטיימר יופיע בצד המסך עם תחילת המבחן.
        * **ציון עובר:** 60 (לפחות 15 תשובות נכונות).
        * **חומר עזר:** ניתן להשתמש בקובץ חקיקה.
        """)
        
        st.write("---")
        
        # אישור וכניסה
        agreed = st.checkbox("אני מאשר/ת את קריאת ההוראות ומוכן/ה להתחיל.")
        
        if not st.session_state.questions:
            exam.fetch_batch(0)
            
        if st.button("התחל בחינה", disabled=not agreed):
            st.session_state.exam_started = True
            st.session_state.current_q_idx = 0
            st.session_state.start_time = time.time()
            st.rerun()
else:
    # ממשק הבחינה
    q_idx = st.session_state.current_q_idx
    questions = st.session_state.questions
    
    # הצגת זמן נותר בצורה ברורה
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, (exam.time_limit * 60) - elapsed)
    mins, secs = divmod(remaining, 60)
    st.sidebar.markdown(f"## זמן נותר: {mins:02d}:{secs:02d}")
    
    if q_idx < len(questions):
        st.subheader(f"שאלה {q_idx + 1} מתוך {exam.total_questions}")
        st.write(questions[q_idx]['q'])
        
        st.radio("בחר/י את התשובה הנכונה:", questions[q_idx]['o'], key=f"q_{q_idx}")
        
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if q_idx > 0 and st.button("שאלה קודמת"):
                st.session_state.current_q_idx -= 1
                st.rerun()
        with col2:
            if q_idx < exam.total_questions - 1:
                if st.button("שאלה הבאה"):
                    if q_idx + 1 == len(questions):
                        exam.fetch_batch(len(questions))
                    st.session_state.current_q_idx += 1
                    st.rerun()
            else:
                if st.button("סיים והגש בחינה"):
                    st.success("הבחינה הוגשה בהצלחה!")
