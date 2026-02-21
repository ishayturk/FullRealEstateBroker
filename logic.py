# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v26 | Date: 22/02/2026 | 00:55
import streamlit as st
import time

def initialize_exam():
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {}
        st.session_state.max_reached = 1
        generate_question(1)

def generate_question(q_number):
    # שאלות דוגמה לבדיקת מבנה (Placeholder)
    bank = {
        1: {
            "question": "על פי חוק המתווכים, מהו התנאי לזכאות לדמי תיווך?",
            "options": ["רישיון בתוקף והיות המתווך גורם יעיל", "חתימה על בלעדיות", "פרסום", "כל התשובות"],
            "correct": 0
        },
        2: {
            "question": "מהו תוקף הבלעדיות המקסימלי לדירת מגורים?",
            "options": ["3 חודשים", "6 חודשים", "9 חודשים", "שנה"],
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

def handle_navigation(direction):
    curr = st.session_state.current_q
    if direction == "next":
        target = curr + 1
        st.session_state.max_reached = max(st.session_state.max_reached, target)
        generate_question(target)
        st.session_state.current_q = target
    elif direction == "prev" and curr > 1:
        st.session_state.current_q -= 1

def get_remaining_seconds():
    if st.session_state.start_time is None: return 5400
    elapsed = time.time() - st.session_state.start_time
    return int(max(0, 5400 - elapsed))

def get_results_data():
    results = []
    score = 0
    for i in range(1, 26):
        q = st.session_state.exam_data.get(i)
        ans = st.session_state.answers_user.get(i)
        correct = (q and ans is not None and ans == q["correct"])
        if correct: score += 4
        results.append({"num": i, "is_correct": correct})
    return score, results

# סוף קובץ
