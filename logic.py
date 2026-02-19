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
            "question_text": "מתווך סיכם עם מוכר על דמי תיווך בגובה 2% בתוספת מע\"מ. המתווך לא החתים את המוכר על הזמנת תיווך בכתב, אך שלח הודעת ווטסאפ עם כל הפרטים והמוכר אישר. האם המתווך זכאי לדמי תיווך?",
            "options": [
                "א. כן, אישור בווטסאפ נחשב כהזמנה בכתב לכל דבר ועניין.",
                "ב. לא, דרישת הכתב בחוק המתווכים היא קוגנטית וצורנית ואינה ניתנת להתנייה.",
                "ג. כן, בתנאי שהמתווך היה הגורם היעיל בעסקה.",
                "ד. כן, אך רק אם המוכר הוא 'לקוח עסקי' ולא אדם פרטי."
            ],
            "correct_index": 1
        }
    ]
    return random.choice(pool)
