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

def get_ethics_prompt():
    return "צור שאלה באתיקה למתווכים בסגנון רשם המתווכים (סיפור מקרה + 4 אפשרויות). החזר JSON."

def generate_question_sync(index):
    """פונקציה לייצור שאלה. במציאות כאן תהיה קריאת ה-AI"""
    # דוגמה לשאלה שתעלה כדי שלא יהיה ריק
    questions_pool = [
        {
            "question_text": "מתווך גבה דמי תיווך מלקוח מבלי שהחתים אותו על טופס הזמנה בכתב, אך העסקה הושלמה והוא היה הגורם היעיל. האם הוא זכאי לשכר?",
            "options": [
                "א. כן, כי הוא היה הגורם היעיל.",
                "ב. לא, חובה להחתים על הזמנה בכתב לפי חוק המתווכים.",
                "ג. כן, אם הלקוח הודה שקיבל שירות.",
                "ד. רק אם מדובר בעסקת שכירות."
            ],
            "correct_index": 1
        }
    ]
    # מחזיר שאלה רנדומלית או מהפול למטרת הבדיקה
    return random.choice(questions_pool)
