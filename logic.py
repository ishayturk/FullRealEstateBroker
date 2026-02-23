# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V215 | Date: 24/02/2026 | 02:00
import streamlit as st
import time
import random

def generate_question_from_engine(q_num):
    # מנוע ייצור שאלות דינמי
    pool = [
        {"q": "מהי תקופת הבלעדיות המקסימלית בדירת מגורים לפי חוק המתווכים?", "correct": "שישה חודשים.", "distractors": ["שנה אחת.", "שלושה חודשים.", "אין הגבלה בחוק."]},
        {"q": "האם מתווך רשאי לבצע פעולות משפטיות עבור לקוחו?", "correct": "לא; חל איסור מוחלט על מתווך לערוך מסמכים בעלי אופי משפטי.", "distractors": ["כן, אם הוא עו"ד במקצועו.", "רק אם קיבל אישור מהלקוח בכתב.", "כן, אך רק זיכרון דברים."]}
    ]
    data = pool[q_num % len(pool)]
    options = [data["correct"]] + data["distractors"]
    random.shuffle(options)
    return {
        "question": f"שאלה {q_num}: " + data["q"],
        "options": options,
        "answer_index": options.index(data["correct"])
    }

def initialize_exam_state():
    if "step" not in st.session_state: st.session_state.step = "instructions"
    if "exam_data" not in st.session_state: st.session_state.exam_data = {}
    if "answers_user" not in st.session_state: st.session_state.answers_user = {}
    if "nav_active_questions" not in st.session_state: st.session_state.nav_active_questions = set()
    if "start_time" not in st.session_state: st.session_state.start_time = time.time()
    if "current_q" not in st.session_state: st.session_state.current_q = 1
    if "finish_button_visible" not in st.session_state: st.session_state.finish_button_visible = False

def ensure_question_exists(q_num):
    if q_num <= 25 and q_num not in st.session_state.exam_data:
        st.session_state.exam_data[q_num] = generate_question_from_engine(q_num)

def get_remaining_seconds():
    elapsed = time.time() - st.session_state.start_time
    remaining = (90 * 60) - elapsed
    return max(0, int(remaining))

# סוף קובץ
