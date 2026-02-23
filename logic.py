# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V218 | Date: 24/02/2026 | 02:50
import streamlit as st
import time
import random

def generate_question_from_engine(q_num):
    pool = [
        {"q": "מי רשאי לקבל רישיון תיווך לפי החוק?", "correct": "אזרח או תושב ישראל, מעל גיל 18, שאינו פושט רגל ועמד בבחינה.", "distractors": ["כל אדם ללא הגבלת גיל.", "רק עורכי דין פעילים.", "מי שעסק בתיווך לפחות שנתיים בחו\"ל."]},
        {"q": "מהי חובת הגילוי של מתווך?", "correct": "לגלות ללקוח כל מידע מהותי הנוגע לנכס נשוא עסקת התיווך.", "distractors": ["רק מה שהמוכר ביקש לגלות.", "מידע שנמצא בטאבו בלבד.", "אין חובת גילוי אם הקונה לא שאל."]}
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
