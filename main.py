# FILE-ID: C-01
import streamlit as st
from logic import ExamLogic
import time

# הגדרות עמוד
st.set_page_config(page_title="סימולטור מבחן מתווכים", layout="wide")

# הזרקת CSS לתיקון יישור לימין (RTL) ועיצוב הסייד-בר
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: RTL; text-align: right; }
    div[role="radiogroup"] { direction: RTL; text-align: right; }
    p, h1, h2, h3, h4, li, div { text-align: right; direction: RTL; }
    [data-testid="stSidebar"] { direction: RTL; text-align: right; }
    /* עיצוב כפתורי הסייד-בר ברשת */
    .stButton button { width: 100%; padding: 5px; font-size: 14px; }
    /* תיקון לטיימר שיהיה בולט */
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# אתחול
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()
    st.session_state.logic.total_seconds = 5400  # 90 דקות בדיוק
    st.session_state.used_exams = []
    st.session_state.current_exam = None
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.start_time = None
    st.session_state.exam_finished = False

def start_new_exam():
    filename, exam_data = st.session_state.logic.select_next_exam(st.session_state.used_exams)
    st.session_state.current_exam = exam_data
    st.session_state.used_exams.append(filename)
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.start_time = time.time()
    st.session_state.exam_finished = False

# --- מסך פתיחה ---
if st.session_state.current_exam is None:
    st.title("מבחן סימולציה לרישיון מתווך")
    st.subheader("הנחיות למהלך הבחינה:")
    
    st.markdown("""
    * משך הבחינה הוא 90 דקות בדיוק.
    * הבחינה כוללת 25 שאלות רב-ברירתיות.
    * לא ניתן להתקדם לשאלה הבאה מבלי לסמן תשובה בשאלה הנוכחית.
    * ניתן לחזור לשאלות קודמות ולתקן את התשובה בכל עת דרך תפריט הניווט.
    * במידה והזמן יסתיים, המערכת תנעל ותשמור את התשובות שסומנו עד לאותו רגע.
    """)
    
    st.divider()
    
    # צ'ק-בוקס אישור
    agreed = st.checkbox("קראתי והבנתי את מהלך הבחינה")
    
    # כפתור התחלה מותנה
    if st.button("התחל בחינה", disabled=not agreed, type="primary"):
        start_new_exam()
        st.rerun()

# --- מסך מבחן פעיל ---
elif not st.session_state.exam_finished:
    exam = st.session_state.current_exam
    questions = exam['questions']
    q_idx = st.session_state.question_index
    current_q = questions[q_idx]
    
    # ניהול זמן בזמן אמת
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, st.session_state.logic.total_seconds - elapsed)
    
    if remaining <= 0:
        st.session_state.exam_finished = True
        st.rerun()

    # --- סייד בר: ניווט בין השאלות ---
    with st.sidebar:
        st.header("ניווט בין השאלות")
        st.write("בחר שאלה למעבר מהיר:")
        
        # יצירת רשת של 4 בשורה
        for i in range(0, len(questions), 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx < len(questions):
                    answered = str(idx) in st.session_state.answers
                    btn_label = f"{idx+1}"
                    # תנאי ניווט: נענה, או נוכחי, או הבא בתור אחרי האחרון שנענה
                    can_
