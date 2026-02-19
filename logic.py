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
    # סימולציה של שאלת אתיקה מורכבת מהקבצים שלך
    questions_pool = [
        {
            "question_text": "המתווך יצחק פרסם דירה בבלעדיות. במהלך תקופת הבלעדיות, הגיע רוכש פוטנציאלי ישירות לבעל הדירה וסגר איתו עסקה. המתווך ביצע 2 פעולות שיווק מתוך הרשימה בתקנות. האם יצחק זכאי לדמי תיווך?",
            "options": [
                "א. כן, בתקופת בלעדיות המתווך תמיד זכאי לדמי תיווך ללא קשר לפעולות השיווק.",
                "ב. לא, עליו לבצע לפחות 3 פעולות שיווק כדי ליהנות מחזקת הגורם היעיל.",
                "ג. כן, מאחר שביצע 2 פעולות שיווק כנדרש בתקנות, קיימת חזקה שהיה הגורם היעיל.",
                "ד. לא, אם הרוכש הגיע ישירות למוכר, חזקת הגורם היעיל מתבטלת אוטומטית."
            ],
            "correct_index": 2
        }
    ]
    return random.choice(questions_pool)
