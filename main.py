import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

# חובה: השורה הראשונה בקוד. הגדרת דף רחב עם סיידבר פתוח.
st.set_page_config(page_title="מערכת בחינות", layout="wide", initial_sidebar_state="expanded")

def apply_ui_fix():
    st.markdown("""
        <style>
            /* הגדרות כלליות ליישור לימין */
            .main .block-container {
                direction: rtl !important;
                text-align: right !important;
            }
            [data-testid="stSidebar"] {
                direction: rtl !important;
                background-color: #f8f9fa;
            }
            .stMarkdown, .stRadio label, p, div, h1, h2, h3, h4, label, .stButton button {
                direction: rtl !important;
                text-align: right !important;
            }
            /* עיצוב הטיימר */
            .custom-timer {
                background: white;
                color: #ff4b4b;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                border: 2px solid #ff4b4b;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar(questions):
    with st.sidebar:
        st.header("ניווט מהיר")
        st.write("---")
        
        # הצגת כפתורי ניווט לשאלות (גריד של 4 עמודות)
        cols = st.columns(4)
        for i in range(len(questions)):
            q_id = str(questions[i]['id'])
            is_answered = q_id in st.session_state.answers
            
            # צבע שונה לשאלה שנענתה (סימון V)
            label = f"{i+1}"
            if is_answered:
                label += " ✓"
            
            if cols[i % 4].button(label, key=f"btn_nav_{i}"):
                st.session_state.q_idx = i
                st.rerun()
        
        st.write("---")
        if st.button("📖 מעבר למצב לימוד"):
            st.info("הכניסה למבחן לא משפיעה על החלק הלימודי.")

def render_timer():
    if 'start_time' not in st.session_state: 
        st.session_state.start_time = time.time()
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(remaining), 60)
    
    st.markdown(f'<div class="custom-timer">⏱️ זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

def render_intro(exam_data):
    info = exam_data.get('exam_info', {})
    st.title(info.get('title', 'בחינת רישוי'))
    st.write("---")
    st.markdown("### הנחיות:")
    st.write(info.get('instructions', "יש לענות על כל השאלות."))
    st.write(f"**מספר שאלות:** {len(exam_data.get('questions', []))}")
    
    agreed = st.checkbox("אני מאשר שקראתי את ההוראות")
    if st.button("התחל בחינה 🚀", disabled=not agreed):
        st.session_state.current_step = 'exam'
        st.session_state.start_time = time.time()
        st.rerun()

def render_exam_flow(exam_data):
    questions = exam_data.get('questions', [])
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    q = questions[st.session_state.q_idx]
    
    st.subheader(f"שאלה {st.session_state.q_idx + 1} מתוך {len(questions)}")
    st.markdown(f"#### {q['q']}")
    
    current_ans = st.session_state.answers.get(str(q['id']), None)
    
    # הצגת אפשרויות
    choice = st.radio("", q['o'], index=q['o'].index(current_ans) if current_ans in q['o'] else None, key=f"q_{st.session_state.q_idx}")
    
    if choice:
        st.session_state.answers[str(q['id'])] = choice

    st.write("---")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.session_state.q_idx > 0:
            if st.button("⬅️ הקודם"):
                st.session_state.q_idx -= 1
                st.rerun()
    with c3:
        answered = str(q['id']) in st.session_state.answers
        if st.session_state.q_idx < len(questions) - 1:
            if st.button("הבא ➡️", disabled=not answered):
                st.session_state.q_idx += 1
                st.rerun()
        else:
            if st.button("סיום והגשה 🏁", disabled=not answered):
                st.session_state.current_step = 'feedback'
                st.rerun()

def render_feedback(exam_data):
    st.title("תוצאות המבחן")
    # לוגיקה מקוצרת לפידבק
    correct = 0
    for q in exam_data['questions']:
        user_ans = st.session_state.answers.get(str(q['id']), "")
        if user_ans.strip().startswith(q['a'].strip()):
            correct += 1
    
    st.metric("ציון סופי", f"{int((correct/len(exam_data['questions']))*100)}")
    if st.button("מבחן חדש"):
        st.session_state.clear()
        st.rerun()

def main():
    apply_ui_fix()
    manager = ExamManager()
    exam_data = manager.load_exam()
    if not exam_data: return

    if 'current_step' not in st.session_state: st.session_state.current_step = 'intro'
    if 'answers' not in st.session_state: st.session_state.answers = {}

    if st.session_state.current_step == 'intro':
        render_intro(exam_data)
    elif st.session_state.current_step == 'exam':
        render_sidebar(exam_data['questions'])
        render_timer()
        render_exam_flow(exam_data)
    elif st.session_state.current_step == 'feedback':
        render_feedback(exam_data)

if __name__ == "__main__":
    main()
