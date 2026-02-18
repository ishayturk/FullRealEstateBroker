import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    # הזרקת התיקון העיצובי - בלי להרוס את הלוגיקה
    st.markdown("""import streamlit as st
import time
from logic import ExamManager

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    st.markdown("""
        <style>
            /* 1. העלמת סיידבר וכותרות מערכת */
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], header {display: none !important;}
            
            /* 2. מרכוז תוכן ל-800px וקביעת כיוון כתיבה לימין */
            .main .block-container {
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
                direction: rtl !important;
                text-align: right !important;
            }

            /* 3. השוואת גודל גופן - שאלה ותשובות */
            .stMarkdown p, .stRadio label {
                font-size: 1.1rem !important;
                line-height: 1.6 !important;
            }
            h3 { font-size: 1.3rem !important; }

            /* 4. יישור רדיו (תשובות) לימין */
            [data-testid="stWidgetLabel"] { text-align: right !important; width: 100%; }
            [data-testid="stRadio"] { direction: rtl !important; }

            /* 5. עיצוב טיימר צף עליון שמתעדכן */
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
    
    exam_data = manager.load_exam()
    if not exam_data:
        st.error("מחפש מבחן... וודא שיש קבצי JSON בתיקייה.")
        return

    # ניהול מצב
    if 'current_step' not in st.session_state: st.session_state.current_step = 'exam'
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

    # טיימר עליון - מתרפרש בכל אינטראקציה
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(remaining), 60)
    st.markdown(f'<div class="custom-timer">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    if st.session_state.current_step == 'exam':
        render_exam_flow(exam_data)
    elif st.session_state.current_step == 'feedback':
        render_feedback(exam_data)

def render_exam_flow(exam_data):
    questions = exam_data.get('questions', [])
    if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
    
    q = questions[st.session_state.q_idx]
    
    # הצגת שאלה (בגודל נורמלי)
    st.markdown(f"**שאלה {st.session_state.q_idx + 1} מתוך {len(questions)}**")
    st.markdown(f"**{q['q']}**")
    
    # ניהול תשובות - יישור לימין וגודל אחיד
    current_ans = st.session_state.answers.get(str(q['id']), None)
    
    # מציאת האינדקס של התשובה שנבחרה בעבר כדי להציג אותה
    try:
        default_idx = q['o'].index(current_ans) if current_ans in q['o'] else None
    except:
        default_idx = None

    choice = st.radio("", q['o'], index=default_idx, key=f"rad_{q['id']}")
    
    if choice:
        st.session_state.answers[str(q['id'])] = choice

    # ניווט
    st.write("") # מרווח
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
        # בדיקה אם התשובה הנכונה מופיעה בתוך התשובה שהמשתמש בחר
        is_correct = user_ans.strip().startswith(q['a'].strip())
        
        if is_correct:
            correct_count += 1
            color = "green"
            icon = "✅"
        else:
            color = "red"
            icon = "❌"
            
        with st.container():
            st.markdown(f"---")
            st.markdown(f"#### שאלה {q['id']} {icon}")
            st.write(f"**השאלה:** {q['q']}")
            st.markdown(f"<p style='color:{color}'><b>מה שענית:</b> {user_ans}</p>", unsafe_allow_html=True)
            if not is_correct:
                # הצגת התשובה הנכונה המלאה מתוך הרשימה
                correct_text = next((opt for opt in q['o'] if opt.strip().startswith(q['a'].strip())), q['a'])
                st.markdown(f"<p style='color:green'><b>התשובה הנכונה:</b> {correct_text}</p>", unsafe_allow_html=True)

    score = int((correct_count/len(exam_data['questions']))*100)
    st.subheader(f"הציון הסופי שלך: {score}")
    
    if st.button("חזרה למבחן חדש"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
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
