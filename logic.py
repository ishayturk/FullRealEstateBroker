# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V213 | Date: 24/02/2026 | 01:30
import streamlit as st
import time
import random

def generate_question_from_engine(q_num):
    # מבוסס על מבנה V206
    pool = [
        {"q": "שמעון המתווך החתים לקוח על בלעדיות ל-8 חודשים בדירת מגורים. בתוך תקופה זו נמכרה הדירה. האם הוא זכאי לעמלה?", "correct": "לא; תקופת הבלעדיות המקסימלית לדירת מגורים היא 6 חודשים.", "distractors": ["כן, כי חתמו על 8 חודשים.", "כן, אם ביצע פעולות שיווק.", "רק אם הוא היה הגורם היעיל."]},
        {"q": "מתווך גילה פגם נסתר בנכס והמוכר אסר עליו לגלות זאת. מה הדין?", "correct": "חובת הגילוי לקונה גוברת על הוראת המוכר.", "distractors": ["עליו לשתוק.", "עליו לדווח למשטרה.", "עליו לבטל את ההסכם בלבד."]}
    ]
    data = pool[q_num % len(pool)]
    opts = [data["correct"]] + data["distractors"]
    random.shuffle(opts)
    return {"question": data["q"], "options": opts, "answer_index": opts.index(data["correct"])}

def initialize_exam_state():
    if "step" not in st.session_state: st.session_state.step = "instructions"
    if "exam_data" not in st.session_state: st.session_state.exam_data = {}
    if "answers_user" not in st.session_state: st.session_state.answers_user = {}
    if "nav_active_questions" not in st.session_state: st.session_state.nav_active_questions = {1}
    if "start_time" not in st.session_state: st.session_state.start_time = time.time()
    if "current_q" not in st.session_state: st.session_state.current_q = 1
    if "finish_button_visible" not in st.session_state: st.session_state.finish_button_visible = False

def ensure_question_exists(q_num):
    if q_num <= 25 and q_num not in st.session_state.exam_data:
        st.session_state.exam_data[q_num] = generate_question_from_engine(q_num)

def get_remaining_seconds():
    return max(0, int((90 * 60) - (time.time() - st.session_state.start_time)))
# סוף קובץ
