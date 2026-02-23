# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V212 | Date: 24/02/2026 | 01:15
import streamlit as st
import time
import random

def generate_question_from_engine(q_num):
    # המנוע משתמש בעוגן 1213 ובלינקים המקצועיים
    pool = [
        {"q": "מהו הדין במקרה בו מתווך פעל ללא הסכם בכתב אך היה הגורם היעיל המכריע בעסקה?", "correct": "המתווך אינו זכאי לדמי תיווך, שכן דרישת הכתב לפי חוק המתווכים היא קוגנטית ומהותית.", "distractors": ["הוא זכאי לשכר ראוי בלבד.", "הוא זכאי לדמי תיווך מלאים מכוח דיני עשיית עושר.", "בית המשפט יחייב את הלקוח ב-50% מהעמלה."]},
        {"q": "תקופת הבלעדיות המרבית בדירת מגורים, במידה ולא הוסכם אחרת בנפרד, היא:", "correct": "שישה חודשים מיום ההזמנה.", "distractors": ["שנה אחת.", "שלושה חודשים.", "תשעה חודשים."]}
    ]
    data = pool[q_num % len(pool)]
    options = [data["correct"]] + data["distractors"]
    random.shuffle(options)
    return {"question": data["q"], "options": options, "answer_index": options.index(data["correct"])}

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
    return max(0, int((90 * 60) - (time.time() - st.session_state.start_time)))
# סוף קובץ
