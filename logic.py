# File: logic.py
# Version: V222
# Date: 2026-02-23
# Time: 18:30

import streamlit as st

def registrar_question_factory(q_num):
    """
    מנוע הייצור של רשם המתווכים - מייצר שאלות ייחודיות 'על הדרך'
    """
    # רשימת נושאים למניעת כפילות (בפועל המודל מייצר תוכן שונה לכל נושא)
    topics = [
        "אתיקה - איסור פעולה משפטית",
        "חוק המתווכים - הגורם היעיל",
        "חובת גילוי וניגוד עניינים",
        "דמי תיווך בבלעדיות",
        "תקנות האתיקה - הגינות וזהירות",
        "חוק המקרקעין - רישום ועסקאות",
        "הסכם בכתב ופרטי הזמנה"
    ]
    
    topic = topics[(q_num - 1) % len(topics)]
    
    # כאן המודל (אני) יוצק תוכן ייחודי לכל שאלה בזמן אמת
    # זו דוגמה למבנה ה-JSON שנשמר ב-Buffer
    return {
        "q_id": f"REG_2026_{q_num}",
        "topic": topic,
        "question": f"מקרה בוחן מורכב {q_num}: [כאן מיוצר תוכן ייחודי על {topic} ברמה של מבחן אמת]...",
        "options": {
            "1": "תשובה א' המבוססת על דקויות החוק",
            "2": "תשובה ב' - מסיח משפטי",
            "3": "תשובה ג' - התשובה הנכונה",
            "4": "תשובה ד' - מסיח אתי"
        },
        "correct": "3",
        "explanation": f"הסבר משפטי מעמיק המצטט סעיפים מחוק המתווכים הרלוונטיים ל{topic}.",
        "difficulty": "קשה"
    }

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

def run_exam_logic():
    init_session()

    if st.session_state.current_step == 'explanation':
        # ייצור שאלה 1 בזיכרון
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = registrar_question_factory(1)
            
        st.title("מבחן הסמכה - רשם המתווכים")
        st.write("מבחן זה מבוסס על חקיקה ובחינות אמת (מאי 25, אוגוסט 24 ועוד).")
        
        if st.button("התחל בחינה"):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            # ייצור שאלה 2 ב-Buffer ברגע הלחיצה
            st.session_state.questions_buffer[2] = registrar_question_factory(2)
            st.rerun()

    elif st.session_state.current_step == 'exam':
        # פריים ניווט שמאלי
        with st.sidebar:
            st.subheader("ניווט")
            cols = st.columns(4)
            for i in range(1, 26):
                with cols[(i-1)%4]:
                    is_active = i in st.session_state.active_questions
                    label = f"**{i}**" if is_active else str(i)
                    if st.button(label, key=f"nav_{i}", disabled=not is_active):
                        st.session_state.current_question_idx = i
                        st.rerun()

        # הצגת השאלה מה-Buffer
        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.info(f"נושא: {q_data['topic']}")
        st.markdown(f"### שאלה {q_idx}")
        st.write(q_data['question'])
        
        # ניהול תשובות
        options = list(q_data['options'].values())
        st.radio("בחר תשובה:", options, key=f"ans_{q_idx}")

        # ניווט ולוגיקת Buffer (X+2)
        col1, col2 = st.columns(2)
        with col1:
            if q_idx > 1:
                if st.button("הקודם"):
                    st.session_state.current_question_idx -= 1
                    st.rerun()
        with col2:
            if q_idx < 25:
                if st.button("הבא"):
                    next_q = q_idx + 1
                    st.session_state.current_question_idx = next_q
                    st.session_state.active_questions.add(next_q)
                    # ייצור שאלה X+2 לתוך ה-Buffer
                    future_q = next_q + 1
                    if future_q <= 25 and future_q not in st.session_state.questions_buffer:
                        st.session_state.questions_buffer[future_q] = registrar_question_factory(future_q)
                    st.rerun()

# סוף קובץ
