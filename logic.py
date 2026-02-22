# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v32 | Date: 22/02/2026 | 15:15
import streamlit as st
import time

def initialize_exam():
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {}
        st.session_state.max_reached = 1
        st.session_state.is_q1_ready = False
        generate_question(1)

def generate_question(q_number):
    bank = {
        1: {
            "question": "על פי חוק המתווכים, מהו התנאי לזכאות לדמי תיווך?",
            "options": ["רישיון בתוקף והיות המתווך גורם יעיל", "חתימה על בלעדיות", "פרסום", "כל התשובות"],
            "correct": 0
        },
        2: {
            "question": "שאלה מספר 2 - האם המתווך רשאי לבצע פעולות משפטיות?",
            "options": ["כן, ללא הגבלה", "לא, חל איסור מוחלט", "רק באישור הלקוח", "רק אם הוא עורך דין"],
            "correct": 1
        }
    }
    
    if q_number not in st.session_state.exam_data:
        if q_number in bank:
            st.session_state.exam_data[q_number] = bank[q_number]
        else:
            st.session_state.exam_data[q_number] = {
                "question": f"שאלה מקצועית מספר {q_number} - תוכן לבדיקה",
                "options": ["תשובה 1", "תשובה 2", "תשובה 3", "תשובה 4"],
                "correct": 0
            }
        
        if q_number == 1:
            st.session_state.is_q1_ready = True

def is_first_question_ready():
    return st.session_state.get("is_q1_ready", False)

def start_exam_logic():
    """פעולות לוגיות ברגע הלחיצה על התחלת בחינה"""
    st.session_state.start_time = time.time()
    st.session_state.step = "exam_run"
    # ייצור שאלה 2 ברקע לפי הפרוטוקול
    generate_question(2)

def handle_navigation(direction):
    # פונקציונליות מנוטרלת כרגע לבקשת המשתמש
    pass

def get_remaining_seconds():
    if st.session_state.start_time is None: return 5400
    elapsed = time.time() - st.session_state.start_time
    return int(max(0, 5400 - elapsed))

def get_results_data():
    score = 0
    results = []
    for i in range(1, 26):
        q = st.session_state.exam_data.get(i)
        ans = st.session_state.answers_user.get(i)
        correct = (q and ans is not None and ans == q["correct"])
        if correct: score += 4
        results.append({"num": i, "is_correct": correct})
    return score, results

# סוף קובץ
