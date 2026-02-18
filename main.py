import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix(remaining_seconds):
    # הזרקת CSS ו-JS לטיימר שרץ עצמאית בדפדפן
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], header {{display: none !important;}}
            
            .main .block-container {{
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
                direction: rtl !important;
                text-align: right !important;
            }}

            .stMarkdown p, .stRadio label {{
                font-size: 1.1rem !important;
                line-height: 1.6 !important;
            }}

            [data-testid="stWidgetLabel"] {{ text-align: right !important; width: 100%; }}
            [data-testid="stRadio"] {{ direction: rtl !important; }}

            .custom-timer {{
                position: fixed; top: 0; left: 0; width: 100%; background: white;
                color: #ff4b4b; text-align: center; padding: 15px;
                font-size: 24px; font-weight: bold; border-bottom: 2px solid #ff4b4b;
                z-index: 9999; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
        </style>
        
        <div class="custom-timer" id="timer-display">טוען זמן...</div>
        
        <script>
            var seconds = {remaining_seconds};
            function updateTimer() {{
                var m = Math.floor(seconds / 60);
                var s = seconds % 60;
                document.getElementById('timer-display').innerHTML = 
                    'זמן נותר: ' + (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
                if (seconds > 0) {{
                    seconds--;
                    setTimeout(updateTimer, 1000);
                }} else {{
                    document.getElementById('timer-display').innerHTML = 'הזמן תם!';
                }}
            }}
            updateTimer();
        </script>
    """, unsafe_allow_html=True)

def main():
    manager = ExamManager()
    exam_data = manager.load_exam()
    
    if not exam_data:
        st.error("מחפש מבחן... וודא שיש קבצי JSON בתיקייה.")
        return

    if 'current_step' not in st.session_state: st.session_state.current_step = 'exam'
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

    # חישוב זמן נותר להזרקה ל-JS
    elapsed = time.time() - st.session_state.start_time
    remaining = int(max(0, (90 * 60) - elapsed))
    
    apply_ui_fix(remaining)

    if st.session_state.current_step == 'exam':
        render_exam_flow(exam_data)
    elif st.session_state.current_step == 'feedback':
        render_feedback(exam_data)

def render_exam_flow(exam_data):
    questions = exam_data.get('questions', [])
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    
    q = questions[st.session_state.q_idx]
    
    st.markdown(f"**שאלה {st.session_state.q_idx + 1} מתוך {len(questions)}**")
    st.markdown(f"**{q['q']}**")
    
    current_ans = st.session_state.answers.get(str(q['id']), None)
    
    try:
        default_idx = q['o'].index(current_ans) if current_ans in q['o'] else None
    except:
        default_idx = None

    choice = st.radio("", q['o'], index=default_idx, key=f"rad_{q['id']}")
    
    if choice:
        st.session_state.answers[str(q['id'])] = choice

    st.write("") 
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
    st.markdown("## סיכום בחינה")
    correct_count = 0
    
    for q in exam_data['questions']:
        user_ans = st.session_state.answers.get(str(q['id']), "לא נענתה")
        is_correct = user_ans.strip().startswith(q['a'].strip())
        
        if is_correct:
            correct_count += 1
            st.markdown(f"**שאלה {q['id']}: ✅**")
        else:
            st.markdown("---")
            st.markdown(f"**שאלה {q['id']}: ❌**")
            st.markdown(f"<p style='color:red; text-align:right;'><b>מה שענית:</b> {user_ans}</p>", unsafe_allow_html=True)
            correct_text = next((opt for opt in q['o'] if opt.strip().startswith(q['a'].strip())), q['a'])
            st.markdown(f"<p style='color:green; text-align:right;'><b>התשובה הנכונה:</b> {correct_text}</p>", unsafe_allow_html=True)

    score = int((correct_count/len(exam_data['questions']))*100)
    st.subheader(f"הציון הסופי שלך: {score}")
    
    if st.button("חזרה למבחן חדש"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
