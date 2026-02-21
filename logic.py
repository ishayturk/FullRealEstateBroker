# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v08 | Date: 21/02/2026 | 23:50
import streamlit as st
import time

def initialize_exam():
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {}
        generate_question(1)

def generate_question(q_number):
    # שאלות מקצועיות לדוגמה
    bank = {
        1: {
            "question": "על פי חוק המתווכים, מהו התנאי לזכאות לדמי תיווך?",
            "options": ["רישיון בתוקף והיות המתווך גורם יעיל", 
                        "חתימה על בלעדיות בלבד", "פרסום הנכס", "כל התשובות"],
            "correct": 0
        },
        2: {
            "question": "מהו תוקף הבלעדיות המקסימלי לדירת מגורים?",
            "options": ["3 חודשים", "6 חודשים", "9 חודשים", "שנה"],
            "correct": 1
        }
    }
    if q_number in bank:
        st.session_state.exam_data[q_number] = bank[q_number]
    else:
        st.session_state.exam_data[q_number] = {
            "question": f"שאלה מקצועית {q_number} בנושא דיני מקרקעין...",
            "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"],
            "correct": 0
        }

def handle_navigation(direction):
    curr = st.session_state.current_q
    if direction == "next":
        target = curr + 1
        if target + 1 <= 25 and (target + 1) not in st.session_state.exam_data:
            generate_question(target + 1)
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
        is_correct = (q and ans is not None and ans == q["correct"])
        if is_correct: score += 4
        results.append({
            "num": i, "is_correct": is_correct,
            "user_text": q["options"][ans] if (q and ans is not None) else "חסר",
            "correct_text": q["options"][q["correct"]] if q else "N/A"
        })
    return score, results

# סוף קובץ
