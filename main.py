import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], header {display: none !important;}
            
            .main .block-container {
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
                direction: rtl !important;
            }

            /* הגדרת יישור לימין לכל אלמנט טקסט */
            .stMarkdown, .stRadio label, p, div, h1, h2, h3, h4 {
                direction: rtl !important;
                text-align: right !important;
            }

            .custom-timer {
                position: fixed; top: 0; left: 0; width: 100%; background: white;
                color: #ff4b4b; text-align: center; padding: 15px;
                font-size: 24px; font-weight: bold; border-bottom: 2px solid #ff4b4b;
                z-index: 9999; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                direction: ltr !important;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_ui_fix()
    manager = ExamManager()
    exam_data = manager.load_exam()
    
    if not exam_data:
        st.error("לא נמצאו נתונים לבחינה.")
        return

    if 'current_step' not in st.session_state: st.session_state.current_step = 'intro'
    if 'answers' not in st.session_state: st.session_state.answers = {}

    if st.session_state.current_step == 'intro':
        render_intro(exam_data)
    
    elif st.session_state.current_step == 'exam':
        if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, (90 * 60) - elapsed)
        mins, secs = divmod(int(remaining), 60)
        st.markdown(f'<div class="custom-timer">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        render_exam_flow(exam_data)
        
    elif st.session_state.current_step == 'feedback':
        render_feedback(exam_data)

def render_intro(exam_data):
    st.markdown("# ברוכים הבאים לבחינה")
    info = exam_data.get('exam_info', {})
    st.info(info.get('instructions', "אנא קרא את השאלות בעיון."))
    st.write(f"**תאריך בחינה:** {info.get('date', 'לא צוין')}")
    st.write("---")
    if st.button("התחל בחינה 🚀"):
        st.session_state.current_step = 'exam'
        st.session_state.start_time = time.time()
        st.rerun()

def render_exam_flow(exam_data):
    questions = exam_data.get('questions', [])
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    q = questions[st.session_state.q_idx]
    
    st.markdown(f"#### שאלה {st.session_state.q_idx + 1} מתוך {len(questions)}")
    st.markdown(f"**{q['q']}**")
    
    current_ans = st.session_state.answers.get(str(q['id']), None)
    try:
        default_idx = q['o'].index(current_ans) if current_ans in q['o'] else None
    except:
        default_idx = None

    choice = st.radio("", q['o'], index=default_idx, key=f"rad_{q['id']}")
    if choice:
        st.session_state.answers[str(q['id'])] = choice

    col1, _, col3 = st.columns([1,1,1])
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
    st.markdown("<h2 style='text-align: right;'>סיכום בחינה ומשוב</h2>", unsafe_allow_html=True)
    correct_count = 0
    
    for q in exam_data['questions']:
        user_ans = st.session_state.answers.get(str(q['id']), "לא נענתה")
        is_correct = user_ans.strip().startswith(q['a'].strip())
        
        if is_correct:
            correct_count += 1
            st.markdown(f"<div style='text-align: right; direction: rtl;'><b>שאלה {q['id']}: ✅</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: right; direction: rtl;'>", unsafe_allow_html=True)
            st.markdown(f"<b>שאלה {q['id']}: ❌</b>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:red;'><b>מה שענית:</b> {user_ans}</p>", unsafe_allow_html=True)
            correct_text = next((opt for opt in q['o'] if opt.strip().startswith(q['a'].strip())), q['a'])
            st.markdown(f"<p style='color:green;'><b>התשובה הנכונה:</b> {correct_text}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    score = int((correct_count/len(exam_data['questions']))*100)
    st.markdown(f"<h3 style='text-align: right;'>הציון הסופי שלך: {score}</h3>", unsafe_allow_html=True)
    
    if st.button("מבחן חדש"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
