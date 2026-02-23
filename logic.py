# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V216 | Date: 24/02/2026 | 02:20
import streamlit as st
import time
import random

def generate_question_from_engine(q_num):
    # מנוע שאלות נקי משגיאות סינטקס
    pool = [
        {"q": "מהי דרישת הכתב לפי סעיף 9 לחוק המתווכים?", "correct": "דרישה מהותית - ללא הזמנה בכתב המתווכים לא יהיה זכאי לדמי תיווך.", "distractors": ["דרישה ראייתית בלבד.", "ניתן להסתפק בהסכמה בעל פה אם יש עדים.", "הדרישה חלה רק בבלעדיות."]},
        {"q": "מי רשאי לעסוק בתיווך מקרקעין בישראל?", "correct": "רק מי שיש לו רישיון בתוקף לפי חוק המתווכים.", "distractors": ["כל אזרח מעל גיל 18.", "רק עורכי דין.", "מי שעבר קורס שיווק בלבד."]}
    ]
    data = pool[q_num % len(pool)]
    opts = [data["correct"]] + data["distractors"]
    random.shuffle(opts)
    return {"question": data["q"], "options": opts, "answer_index": opts.index(data["correct"])}

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
    elapsed = time.time() - st.session_state.get("start_time", time.time())
    return max(0, int((90 * 60) - elapsed))
# סוף קובץ
