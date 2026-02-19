# FILE-ID: C-01
import streamlit as st
from logic import ExamLogic
import time

# הגדרות עמוד
st.set_page_config(page_title="סימולטור מבחן מתווכים", layout="wide")

# הזרקת CSS לתיקון RTL, מסגרת לצ'ק-בוקס וסידור כפתורים
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: RTL; text-align: right; }
    div[role="radiogroup"] { direction: RTL; text-align: right; }
    p, h1, h2, h3, h4, li, div { text-align: right; direction: RTL; }
    [data-testid="stSidebar"] { direction: RTL; text-align: right; }
    
    /* מסגרת והדגשה לצ'ק-בוקס */
    .checkbox-container {
        border: 2px solid #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        background-color: #fafafa;
        margin-bottom: 20px;
    }
    .stCheckbox label {
        font-weight: bold;
        padding-right: 10px; /* מרווח בין הריבוע למלל */
    }

    /* עיצוב כפתורי הסייד-בר */
    .stButton button { width: 100%; padding: 5px; font-size: 14px; }
    .stMetric { background-color: #f8f9fb; padding: 10px; border-radius: 10px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# אתחול
if 'logic' not in st.session_state:
    st.session_state.logic = ExamLogic()
    st.session_state.logic.total_seconds = 5400  # 90 דקות
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
    * משך הבחינה הוא **90 דקות**.
    * הבחינה כוללת **25 שאלות** רב-ברירתיות.
    * לא ניתן להתקדם לשאלה הבאה מבלי לסמן תשובה.
    * ניתן לחזור לשאלות קודמות דרך תפריט הניווט.
    * בסיום הזמן, המערכת תשמור אוטומטית את מה שסומן.
    """)
    
    st.write("") 
    
    # מסגרת לצ'ק-בוקס
    st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
    agreed = st.checkbox("קראתי והבנתי את מהלך הבחינה")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("התחל בחינה", disabled=not agreed, type="primary"):
        start_new_exam()
        st.rerun()

# --- מסך מבחן פעיל ---
elif not st.session_state.exam_finished:
    exam = st.session_state.current_exam
    questions = exam['questions']
    q_idx = st.session_state.question_index
    current_q = questions[q_idx]
    
    # טיימר
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, st.session_state.logic.total_seconds - elapsed)
    if remaining <= 0:
        st.session_state.exam_finished = True
        st.rerun()

    # --- סייד בר: ניווט בין השאלות (4 בשורה) ---
    with st.sidebar:
        st.header("ניווט בין השאלות")
        for i in range(0, len(questions), 4):
            cols = st.columns(4)
            for j in range(4):
                idx = i + j
                if idx < len(questions):
                    answered = str(idx) in st.session_state.answers
                    # לוגיקת ניווט מתוקנת (מונעת NameError)
                    can_nav = answered or idx == q_idx or (idx > 0 and str(idx-1) in st.session_state.answers)
                    
                    if cols[j].button(f"{idx+1}", key=f"nav_{idx}", disabled=not can_nav, 
                                      type="primary" if answered else "secondary"):
                        st.session_state.question_index = idx
                        st.rerun()
        
        st.divider()
        if len(st.session_state.answers) == len(questions):
            if st.button("🏁 סיים בחינה", key="side_fin"):
                st.session_state.exam_finished = True
                st.rerun()

    # --- תצוגת השאלה והטיימר ---
    c_time, c_title = st.columns([1, 3])
    with c_time:
        st.metric("זמן נותר", st.session_state.logic.format_time(remaining))
    with c_title:
        st.subheader(f"שאלה {q_idx + 1} מתוך {len(questions)}")

    st.info(current_q['question_text'])

    saved_val = st.session_state.answers.get(str(q_idx))
    choice = st.radio("בחר תשובה:", current_q['options'], 
                      index=current_q['options'].index(saved_val) if saved_val else None,
                      key=f"r_{q_idx}")

    if choice:
        st.session_state.answers[str(q_idx)] = choice

    st.divider()

    # כפתורי ניווט תחתונים
    c1, cf, c2 = st.columns([1, 1, 1])
    has_ans = str(q_idx) in st.session_state.answers
    
    with c1:
        if st.button("⬅️ קודמת", disabled=(q_idx == 0)):
            st.session_state.question_index -= 1
            st.rerun()
    with c2:
        if st.button("הבאה ➡️", disabled=(not has_ans or q_idx == len(questions)-1)):
            st.session_state.question_index += 1
            st.rerun()
    with cf:
        if len(st.session_state.answers) == len(questions):
            if st.button("🏁 סיום", type="primary"):
                st.session_state.exam_finished = True
                st.rerun()

else:
    st.title("סיום המבחן")
    st.success("המבחן הושל
