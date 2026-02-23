# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V219 | Date: 23/02/2026 | 16:50
import streamlit as st
import time
import json
import os

# העוגן 1213 והלוגיקה של המבחן (מבוסס פרוטוקול C-01)
def load_exam_questions():
    # לוגיקה לטעינת שאלות מתוך exams_data כפי שסוכם
    # כרגע מדמה שליפה מהעוגן 1213
    try:
        # כאן תבוא הלוגיקה של שליפת הקובץ test_[event]...json
        pass
    except:
        pass

def generate_question_from_engine(q_num):
    # שחזור הלוגיקה לפיה השאלה נגזרת מהעוגן 1213
    # לצורך תקינות הקוד, אני משתמש במבנה נתונים שמתבסס על תוכן העוגן
    anchor_data = [
        {"q": "לפי חוק המתווכים, מהו התנאי המהותי לזכאות לדמי תיווך?", "a": "הזמנה בכתב חתומה על ידי הלקוח.", "d": ["הסכמה בעל פה.", "פרסום הנכס בעיתון.", "שיחה טלפונית עם המוכר."]},
        {"q": "מהו הגורם היעיל לפי הפסיקה?", "a": "המתווך שהיה הגורם המרכזי שהביא להתקשרות הצדדים בעסקה.", "d": ["המתווך הראשון שהראה את הנכס.", "המתווך שדרש את העמלה הנמוכה ביותר.", "המתווך שפרסם את המודעה הכי הרבה זמן."]}
    ]
    data = anchor_data[q_num % len(anchor_data)]
    options = [data["a"]] + data["d"]
    # כאן נשמרת הלוגיקה של ערבוב האופציות
    import random
    random.seed(q_num + 1213) # שימוש בעוגן כ-seed
    random.shuffle(options)
    return {"question": data["q"], "options": options, "answer_index": options.index(data["a"])}

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
