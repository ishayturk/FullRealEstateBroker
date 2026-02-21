# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v07 | Date: 21/02/2026 | 23:40
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
    # תוכן מקצועי אמיתי
    bank = {
        1: {
            "question": "מי רשאי למכור נדל\"ן עבור אחר בתמורה על פי חוק?",
            "options": ["עורך דין", "מתווך בעל רישיון בתוקף", "כל אדם", "שמאי"],
            "correct": 1
        },
        2: {
            "question": "מהו הגורם היעיל בעסקה?",
            "options": ["הראשון שפרסם", "מי שהביא לחתימת הסכם", "מי שערך סיור", "הזול ביותר"],
            "correct": 1
        }
    }
    if q_number in bank:
        st.session_state.exam_data[q_number] = bank[q_number]
    else:
        st.session_state.exam_data[q_number] = {
            "question": f"שאלה מקצועית {q_number}...",
            "options": ["א'", "ב'", "ג'", "ד'"],
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

def get_timer_display():
    if st.session_state.start_time is None: return "90:00"
    rem = max(0, (90 * 60) - (time.time() - st.session_state.start_time))
    mins, secs = divmod(int(rem), 60)
    return f"{mins:02d}:{secs:02d}"

def check_exam_status():
    if st.session_state.start_time is None: return False
    return (time.time() - st.session_state.start_time) >= (90 * 60)

def get_results_data():
    results = []
    score = 0
    for i in range(1, 26):
        q = st.session_state.exam_data.get(i)
        ans = st.session_state.answers_user.get(i)
        correct = (q and ans is not None and ans == q["correct"])
        if correct: score += 4
        results.append({
            "num": i, "is_correct": correct,
            "user_text": q["options"][ans] if (q and ans is not None) else "חסר",
            "correct_text": q["options"][q["correct"]] if q else "N/A"
        })
    return score, results

# סוף קובץ
