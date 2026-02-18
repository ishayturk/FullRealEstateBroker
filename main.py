import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    # הזרקת התיקון העיצובי - בלי להרוס את הלוגיקה
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], header {display: none !important;}
            .main .block-container {
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
            }
            .custom-timer {
                position: fixed; top: 0; left: 0; width: 100%; background: white;
                color: #ff4b4b; text-align: center; padding: 15px;
                font-size: 24px; font-weight: bold; border-bottom: 2px solid #ff4b4b;
                z-index: 9999; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_ui_fix()
    manager = ExamManager()
    
    # 1. לוגיקה של כניסה ובחירת מבחן
    exam_data = manager.load_exam()
    if not exam_data:
        st.error("מחפש מבחן... וודא שיש קבצי JSON בתיקייה.")
        return

    # 2. ניהול מצב המבחן (Session State)
    if 'current_step' not in st.session_state: st.session_state.current_step = 'exam'
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

    # 3. טיימר עליון (התיקון החדש)
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(remaining), 60)
    st.markdown(f'<div class="custom-timer">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # 4. ניווט וניהול שלבים (כניסה/בחינה/משוב)
    if st.session_state.current_step == 'exam':
        render_exam_flow(exam_data)
    elif st.session_state.current_step == 'feedback':
        render_feedback(exam_data)

def render_exam_flow(exam_data):
    questions = exam_data.get('questions', [])
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    
    q = questions[st.session_state.q_idx]
    
    # הצגת התוכן (בלי כותרות מיותרות)
    st.info(f"שאלה {st.session_state.q_idx + 1} מתוך {len(questions)}")
    st.write(f"### {q['q']}")
    
    # לוגיקה של תשובות - שמירה ב-session_state
    current_ans = st.session_state.answers.get(str(q['id']), None)
    choice = st.radio("בחר תשובה:", q['o'], index=None if current_ans is None else q['o'].index(current_ans), key=f"rad_{q['id']}")
    
    if choice:
        st.session_state.answers[str(q['id'])] = choice

    # 5. מערכת ניווט (הבא/הקודם/סיום)
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.session_state.q_idx > 0:
            if st.button("⬅️ הקודם"):
                st.session_state.q_idx -= 1
                st.rerun()
    with col3:
        if st.session_state.q_idx < len(questions) - 1:
            if st.button("הבא ➡️"):
                st.session_state.q_idx += 1
                st.rerun()
        else:
            if st.button("סיום והגשה 🏁"):
                st.session_state.current_step = 'feedback'
                st.rerun()

def render_feedback(exam_data):
    st.header("סיכום בחינה ומשוב")
    # כאן נכנסת לוגיקת חישוב הציון והשוואת תשובות שהגדרנו
    correct_count = 0
    for q in exam_data['questions']:
        user_ans = st.session_state.answers.get(str(q['id']), "לא נענה")
        is_correct = user_ans.startswith(q['a']) # מניח שהתשובה ב-JSON היא האות (א, ב, ג...)
        if is_correct: correct_count += 1
        
        with st.expander(f"שאלה {q['id']} - {'✅' if is_correct else '❌'}"):
            st.write(f"השאלה: {q['q']}")
            st.write(f"התשובה שלך: {user_ans}")
            st.write(f"התשובה הנכונה: {q['a']}")

    st.success(f"סיימת! הציון שלך: {int((correct_count/len(exam_data['questions']))*100)}")
    if st.button("בחינה חדשה"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
