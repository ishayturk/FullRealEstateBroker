# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v10 | Date: 22/02/2026 | 00:05
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
    bank = {
        1: {
            "question": "מהו התנאי המרכזי לזכאות מתווך לדמי תיווך?",
            "options": ["רישיון בתוקף והיותו הגורם היעיל", "פרסום בעיתון", 
                        "שיחה טלפונית", "הסכם בעל פה"],
            "correct": 0
        },
        2: {
            "question": "על פי חוק המתווכים, מהו תוקף בלעדיות מקסימלי?",
            "options": ["3 חודשים", "6 חודשים", "9 חודשים", "שנה"],
            "correct": 1
        }
    }
    if q_number in bank:
        st.session_state.exam_data[q_number] = bank[q_number]
    else:
        st.session_state.exam_data[q_number] = {
            "question": f"שאלה מקצועית {q_number}...",
            "options": ["אופציה 1", "אופציה 2", "אופציה 3", "אופציה 4"],
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

def get_timer_text():
    if st.session_state.start_time is None: return "90:00"
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 5400 - elapsed)
    mins, secs = divmod(int(rem), 60)
    return f"{mins:02d}:{secs:02d}"

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
