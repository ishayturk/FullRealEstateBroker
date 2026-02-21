# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v04 | Date: 21/02/2026 | 23:45
import streamlit as st
import time

def initialize_exam():
    """אתחול משתני המערכת בזיכרון"""
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {}
        # טעינת שאלה ראשונה
        generate_question(1)

def generate_question(q_number):
    """ייצור שאלה מקצועית"""
    # סימולציה של שאלות מקצועיות
    bank = {
        1: {
            "question": "מי מהבאים רשאי לעסוק בתיווך מקרקעין על פי חוק?",
            "options": [
                "מי שסיים לימודי משפטים",
                "בעל רישיון תיווך בתוקף בלבד",
                "כל אזרח מעל גיל 18",
                "סוכן נדל\"ן הרשום באיגוד המתווכים"
            ],
            "correct": 1
        },
        2: {
            "question": "מהו הגורם היעיל בעסקת מקרקעין?",
            "options": [
                "מי שפרסם את המודעה ראשון",
                "מי שהביא לחתימת הסכם מחייב בין הצדדים",
                "מי שערך את סיור הנכס הראשון",
                "מי שגבה את המקדמה"
            ],
            "correct": 1
        }
    }
    
    if q_number in bank:
        st.session_state.exam_data[q_number] = bank[q_number]
    else:
        st.session_state.exam_data[q_number] = {
            "question": f"שאלה מקצועית מספר {q_number} - בייצור...",
            "options": ["תשובה 1", "תשובה 2", "תשובה 3", "תשובה 4"],
            "correct": 0
        }

def handle_navigation(direction):
    """ניהול מעברים ולוגיקת n+2"""
    curr = st.session_state.current_q
    if direction == "next":
        target = curr + 1
        n_load = target + 1
        if n_load <= 25 and n_load not in st.session_state.exam_data:
            generate_question(n_load)
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
            "user_text": q["options"][ans] if (q and ans is not None) else "לא נענתה",
            "correct_text": q["options"][q["correct"]] if q else "N/A"
        })
    return score, results

# סוף קובץ
