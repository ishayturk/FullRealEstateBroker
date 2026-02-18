# exam_logic.py | Version: C-01
import streamlit as st
import random

# בנק שאלות ראשוני (נרחיב אותו בהמשך)
EXAM_QUESTIONS = [
    {
        "question": "מתווך במקרקעין ביצע פעולת תיווך ללא הזמנה בכתב. מהן ההשלכות?",
        "options": ["הוא זכאי לדמי תיווך כרגיל", "הוא אינו זכאי לדמי תיווך", "הלקוח חייב לשלם רק חצי", "זה תלוי בהחלטת בית משפט"],
        "answer": "הוא אינו זכאי לדמי תיווך"
    },
    {
        "question": "מהי תקופת הבלעדיות המקסימלית בדירת מגורים לפי חוק המתווכים?",
        "options": ["3 חודשים", "6 חודשים", "9 חודשים", "שנה"],
        "answer": "6 חודשים"
    }
]

def run_exam():
    st.subheader("📝 מבחן תרגול מקיף")
    
    if "current_exam_questions" not in st.session_state:
        # הגרלה של שאלות מתוך הבנק
        sampled = random.sample(EXAM_QUESTIONS, min(len(EXAM_QUESTIONS), 25))
        st.session_state.current_exam_questions = sampled
        st.session_state.user_answers = {}
        st.session_state.exam_submitted = False

    for i, q in enumerate(st.session_state.current_exam_questions):
        st.write(f"**שאלה {i+1}:** {q['question']}")
        st.session_state.user_answers[i] = st.radio(
            f"בחר תשובה לשאלה {i+1}:", 
            q['options'], 
            key=f"exam_q_{i}", 
            index=None,
            disabled=st.session_state.exam_submitted
        )

    if not st.session_state.exam_submitted:
        if st.button("הגש מבחן"):
            st.session_state.exam_submitted = True
            st.rerun()
    else:
        score = 0
        for i, q in enumerate(st.session_state.current_exam_questions):
            if st.session_state.user_answers.get(i) == q['answer']:
                score += 1
        
        st.success(f"סיימת! הציון שלך: {score}/{len(st.session_state.current_exam_questions)}")
        
        if st.button("חזרה לתפריט ובצע מבחן חדש"):
            for key in list(st.session_state.keys()):
                if key.startswith("exam_q_") or key in ["current_exam_questions", "user_answers", "exam_submitted"]:
                    del st.session_state[key]
            st.session_state.step = "menu"
            st.rerun()
