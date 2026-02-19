import streamlit as st
import random
import time

def initialize_exam():
    if 'exam_state' not in st.session_state:
        st.session_state.exam_state = {
            'questions': [], # רשימת השאלות שנוצרו
            'current_index': -1, # -1 אומר דף הסבר
            'answers': {}, # תשובות המשתמש
            'start_time': None,
            'is_finished': False,
            'next_ready_question': None # השאלה שנוצרה מראש ברקע
        }

def get_ethics_prompt():
    return """
    פעל ככותב בחינות בכיר של רשם המתווכים במשרד המשפטים.
    צור שאלה אחת חדשה לחלוטין בפורמט "סיפור מקרה" (Case Study).
    
    הנחיות קריטיות:
    1. נושא: אתיקה מקצועית, חוק המתווכים, חזקת הגורם היעיל, או ניגוד עניינים בלבד.
    2. סגנון: השתמש בשפה משפטית רשמית כמו בקבצי המבחן (למשל: "מה הדין במקרה זה?", "האם פעל כדין?").
    3. אל תשתמש בשאלות כלליות על מקרקעין שלא קשורות לתיווך.
    4. תשובות: 4 אפשרויות. כל אפשרות כוללת תשובה ונימוק משפטי.
    5. מקוריות: אל תחזור על שאלות קודמות. שנה שמות דמויות ונסיבות.
    
    החזר פורמט JSON בלבד:
    {
      "question_text": "...",
      "options": ["...", "...", "...", "..."],
      "correct_index": 0-3
    }
    """

def fetch_next_question_from_ai():
    # כאן מתבצעת הקריאה ל-LLM (סימולציה לצורך הקוד, בפועל המערכת תשתמש ב-GenerateContent)
    # לצורך הדגמה, המערכת תייצר כאן שאלות אתיקה מבוססות חוק
    pass
