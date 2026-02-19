import streamlit as st
import json

def get_ethics_prompt():
    return """
    פעל ככותב בחינות בכיר של רשם המתווכים. צור שאלה אחת חדשה בפורמט "סיפור מקרה".
    נושאים: אתיקה, חוק המתווכים, הגורם היעיל, וניגוד עניינים בלבד.
    מבנה: שאלה ו-4 אפשרויות עם נימוק משפטי לכל אחת.
    החזר JSON בלבד: {"question_text": "...", "options": ["...", "...", "...", "..."], "correct_index": 0}
    וודא שהתוכן חדש ולא חוזר על עצמו.
    """

def generate_question():
    # כאן המערכת קוראת ל-Gemini (בפועל יש להשתמש ב-model.generate_content)
    # לצורך הדגמה, הפונקציה מחזירה מבנה ריק שה-AI ימלא בזמן אמת
    try:
        # כאן תבוא הפקודה: response = model.generate_content(get_ethics_prompt())
        # ופענוח ה-JSON מהתשובה
        pass
    except:
        return None

def initialize_exam():
    if 'exam_state' not in st.session_state:
        st.session_state.exam_state = {
            'questions': [],
            'current_index': -1,
            'answers': {},
            'start_time': None,
            'is_finished': False,
            'prefetched_next': None,
            'confirmed_instructions': False
        }
