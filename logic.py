import streamlit as st
import random

def initialize_exam():
    if 'exam_state' not in st.session_state:
        st.session_state.exam_state = {
            'questions': [],
            'current_index': -1,
            'answers': {},
            'start_time': None,
            'is_finished': False,
            'confirmed_instructions': False
        }

def generate_question_sync(index):
    pool = [
        {
            "question_text": "מתווך המועסק במשרד תיווך גילה מידע מהותי על ליקוי בנכס שלא היה ידוע לבעלים. מה חובתו לפי חוק המתווכים?",
            "options": [
                "א. חובה לגלות לקונה הפוטנציאלי בלבד.",
                "ב. אין חובה לגלות מידע שהבעלים עצמו לא ידע עליו.",
                "ג. חובה לנהוג בהגינות ולמסור ללקוח כל מידע מהותי הנוגע לנכס.",
                "ד. המתווך רשאי לשתוק כדי לא לפגוע בסיכויי העסקה."
            ],
            "correct_index": 2
        }
    ]
    return random.choice(pool)
