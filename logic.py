# File: logic.py
# Version: V221
# Date: 2026-02-23
# Time: 18:02

import streamlit as st
import json

def get_registrar_question(q_num):
    """
    מנוע רשם המתווכים - ייצור שאלה מורכבת מבוססת מקרי בוחן (פרוטוקול C-01)
    מבוסס על בחינות: מאי 25, יולי 25, פברואר 25, אוגוסט 24
    """
    # דוגמה לייצור שאלה מבוססת ידע משפטי ואתיקה
    questions_pool = {
        1: {
            "q_id": "MAY25_Q1",
            "topic": "אתיקה מקצועית - איסור פעולה משפטית",
            "question": "המתווכת דניאלה ליוותה את הצדדים בעסקת מכר. לאחר שהסכימו על המחיר, הכינה דניאלה 'זיכרון דברים' מפורט הכולל את מועד המסירה וגובה הפיצוי המוסכם, והחתימה את הצדדים. הלקוח מסרב לשלם דמי תיווך בטענה שדניאלה הפרה את החוק. האם דניאלה זכאית לדמי תיווך?",
            "options": {
                "1": "כן, שכן מדובר בזיכרון דברים בלבד ולא בחוזה מכר סופי.",
                "2": "לא, מאחר שסייעה בעריכת מסמך בעל אופי משפטי בניגוד לסעיף 12 לחוק.",
                "3": "כן, בתנאי שהייתה הגורם היעיל בעסקה והצדדים חתמו מרצונם.",
                "4": "לא, אלא אם קיבלה אישור מראש ובכתב מעורך הדין של אחד הצדדים."
            },
            "correct": "2",
            "explanation": "סעיף 12 לחוק המתווכים אוסר על מתווך לסייע בעריכת מסמכים משפטיים. הפרה זו שוללת זכאות לדמי תיווך.",
            "difficulty": "קשה"
        },
        2: {
            "q_id": "AUG24_Q2",
            "topic": "חוק המתווכים - בלעדיות ופעולות שיווק",
            "question": "מתווך קיבל בלעדיות למכירת נכס למשך 6 חודשים. בחודש החמישי הלקוח מכר את הנכס בעצמו לקונה שלא הגיע דרך המתווך. המתווך ביצע רק פעולת שיווק אחת (שלט על הנכס). האם הוא זכאי לדמי תיווך?",
            "options": {
                "1": "כן, חזקת הגורם היעיל בבלעדיות היא מוחלטת לכל תקופת ההסכם.",
                "2": "לא, שכן המתווך לא ביצע לפחות שתי פעולות שיווק כנדרש בתקנות.",
                "3": "כן, אם הלקוח מנע ממנו לבצע פעולות נוספות.",
                "4": "לא, בבלעדיות המתווך זכאי לדמי תיווך רק אם הוא זה שהביא את הקונה בפועל."
            },
            "correct": "2",
            "explanation": "כדי ליהנות מחזקת הגורם היעיל בבלעדיות, על המתווך לבצע לפחות שתי פעולות שיווק הקבועות בתקנות.",
            "difficulty": "קשה"
        }
    }
    return questions_pool.get(q_num, questions_pool[1]) # ברירת מחדל לשאלה 1 לצורך הדגמה

def init_session():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'explanation'
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 1
    if 'questions_buffer' not in st.session_state:
        st.session_state.questions_buffer = {}
    if 'active_questions' not in st.session_state:
        st.session_state.active_questions = set()
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

def render_logic():
    init_session()
    
    # CSS מופרד (General, Desktop, Mobile)
    st.markdown("""
        <style>
        /* General */
        .stRadio > label { font-weight: bold; }
        
        /* Desktop */
        @media (min-width: 1024px) {
            .main { direction: rtl; }
        }
        
        /* Mobile */
        @media (max-width: 1023px) {
            .main { padding: 10px; }
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.current_step == 'explanation':
        # ייצור שאלה 1 בעמוד ההסבר
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = get_registrar_question(1)
            
        st.title("מבחן רשם המתווכים - הסברים")
        if st.button("התחל בחינה"):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            # לחיצה מייצרת את שאלה 2 ברקע
            st.session_state.questions_buffer[2] = get_registrar_question(2)
            st.rerun()

    elif st.session_state.current_step == 'exam':
        # פריים ניווט משמאל
        with st.sidebar:
            st.write("### ניווט")
            cols = st.columns(4)
            for i in range(1, 26):
                with cols[(i-1)%4]:
                    is_active = i in st.session_state.active_questions
                    label = f"**{i}**" if is_active else str(i)
                    if st.button(label, key=f"nav_{i}", disabled=not is_active):
                        st.session_state.current_question_idx = i
                        st.rerun()

        # פריים תוכן
        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.info(f"נושא: {q_data['topic']}")
        st.write(f"**שאלה {q_idx}:**")
        st.write(q_data['question'])
        
        ans = st.radio("בחר תשובה:", list(q_data['options'].values()), 
                       index=None, key=f"radio_{q_idx}")
        
        if ans:
            # שמירת התשובה במילון
            for k, v in q_data['options'].items():
                if v == ans:
                    st.session_state.user_answers[q_idx] = k

        # כפתור הבא ולוגיקת Buffer
        if st.button("לשאלה הבאה"):
            if q_idx < 25:
                next_idx = q_idx + 1
                st.session_state.current_question_idx = next_idx
                st.session_state.active_questions.add(next_idx)
                
                # ייצור X+2
                future_idx = next_idx + 1
                if future_idx <= 25 and future_idx not in st.session_state.questions_buffer:
                    st.session_state.questions_buffer[future_idx] = get_registrar_question(future_idx)
                st.rerun()

# סוף קובץ
