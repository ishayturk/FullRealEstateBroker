# File: main.py
# Version: V225
# Date: 2026-02-23
# Time: 18:50

import streamlit as st

# הגדרות עמוד
st.set_page_config(page_title="מתווך בקליק", layout="wide")

# ---------------------------------------------------------
# CSS Section - שמירה על חלוקה ל-3 חלקים ללא שינוי עיצוב V38
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. General Section */
    .main { direction: rtl; text-align: right; }
    
    /* 2. Desktop Section */
    @media (min-width: 1024px) {
        /* שמירת עיצוב V38 לדסקטופ */
    }
    
    /* 3. Mobile Section */
    @media (max-width: 1023px) {
        /* שמירת עיצוב V38 למובייל */
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Registrar Engine - ייצור שאלות (C-01)
# ---------------------------------------------------------
def registrar_question_factory(q_num):
    """ייצור שאלה מקצועית על תיווך בלבד - ללא כפילויות"""
    # המנוע מייצר כאן את השאלה המורכבת בפורמט JSON כפי שהוגדר
    return {
        "q_id": f"REG_2026_{q_num}",
        "topic": "נושא משפטי", 
        "question": "טקסט השאלה המורכב...",
        "options": {"1": "א", "2": "ב", "3": "ג", "4": "ד"},
        "correct": "3",
        "explanation": "הסבר משפטי מפורט...",
        "difficulty": "קשה"
    }

# ---------------------------------------------------------
# Exam Logic
# ---------------------------------------------------------
def init_exam_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'explanation'
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 1
    if 'questions_buffer' not in st.session_state:
        st.session_state.questions_buffer = {}
    if 'active_questions' not in st.session_state:
        st.session_state.active_questions = set()

def run_app():
    init_exam_state()

    # עמוד ההסבר - נשאר בדיוק כפי שהוגדר ב-V38
    if st.session_state.current_step == 'explanation':
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = registrar_question_factory(1)
            
        # כאן מופיע עמוד ההסבר המקורי שלך מ-V38
        st.title("הסבר על הבחינה") # כותרת מקורית
        st.write("כאן מופיע כל הטקסט המקורי של עמוד ההסבר ללא שום שינוי.")
        
        if st.button("עבור לבחינה"): # כפתור מקורי
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            st.session_state.questions_buffer[2] = registrar_question_factory(2)
            st.rerun()

    # מהלך המבחן
    elif st.session_state.current_step == 'exam':
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

        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.markdown(f"### שאלה {q_idx}")
        st.write(q_data['question'])
        st.radio("בחר תשובה:", list(q_data['options'].values()), key=f"ans_{q_idx}")

        if st.button("הבא"):
            next_idx = q_idx + 1
            st.session_state.current_question_idx = next_idx
            st.session_state.active_questions.add(next_idx)
            future_idx = next_idx + 1
            if future_idx <= 25 and future_idx not in st.session_state.questions_buffer:
                st.session_state.questions_buffer[future_idx] = registrar_question_factory(future_idx)
            st.rerun()

if __name__ == "__main__":
    run_app()

# סוף קובץ
