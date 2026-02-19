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
    # שאלת דמה איכותית מאתיקה
    questions_pool = [
        {
            "question_text": "מתווך במקרקעין הציע לנכס שבטיפולו קונה שהוא אחיו של המתווך. המתווך לא גילה למוכר את הקשר המשפחתי. מה הדין?",
            "options": [
                "א. פעל כדין אם המחיר הוא מחיר שוק.",
                "ב. הפר את חובת הגילוי ופעל בניגוד עניינים.",
                "ג. מותר אם הוא גובה דמי תיווך רק מהמוכר.",
                "ד. מותר אם האח חתם על טופס הזמנת תיווך נפרד."
            ],
            "correct_index": 1
        }
    ]
    return random.choice(questions_pool)
