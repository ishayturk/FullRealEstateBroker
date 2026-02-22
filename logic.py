# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v35 | Date: 22/02/2026 | 18:10
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
        st.session_state.nav_active_questions = set() 
        generate_question(1)

def generate_question(q_number):
    bank = {
        1: {
            "question": "על פי חוק המתווכים, מהו התנאי לזכאות לדמי תיווך?",
            "options": ["רישיון בתוקף והיות המתווך גורם יעיל", "חתימה על בלעדיות", "פרסום", "כל התשובות"],
            "correct": 0
        },
        2: {
            "question": "האם המתווך רשאי לבצע פעולות משפטיות?",
            "options": ["כן, ללא הגבלה", "לא, חל איסור מוחלט", "רק באישור הלקוח", "רק אם הוא עורך דין"],
            "correct": 1
        }
    }
    
    if q_number not in st.session_state.exam_data:
        if q_number in bank:
            st.session_state.exam_data[q_number] = bank[q_number]
        else:
            st.session_state.exam_data[q_number] = {
                "question": f"תוכן מקצועי לשאלה {q_number} המדמה אורך של כמה שורות לצורך בחינת העיצוב והמרווחים.",
                "options": ["תשובה 1", "תשובה 2", "תשובה 3", "תשובה 4"],
                "correct": 0
            }
        
        if q_number == 1:
            st.session_state.is_q1_ready = True

def is_first_question_ready():
    return st.session_state.get("is_q1_ready", False)

def start_exam_logic():
    st.session_state.start_time = time.time()
    st.session_state.step = "exam_run"
    generate_question(2)

def move_to_next():
    current = st.session_state.current_q
    st.session_state.nav_active_questions.add(current)
    st.session_state.current_q += 1
    if st.session_state.current_q > st.session_state.max_reached:
        st.session_state.max_reached = st.session_state.current_q
        generate_question(st.session_state.current_q + 1)

def get_remaining_seconds():
    if st.session_state.get("start_time") is None:
        return 5400
    elapsed = time.time() - st.session_state.start_time
    return max(0, 5400 - int(elapsed))

# סוף קובץ
