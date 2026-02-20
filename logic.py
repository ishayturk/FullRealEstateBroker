import google.generativeai as genai
import streamlit as st
import json
import re

# פרומפט בחינה "יבש" - ממוקד יצירת שאלה אחת בלבד
EXAM_PROMPT = """
As an expert in the Israeli Real Estate Brokers Exam, generate ONE multiple-choice question.
Rules:
1. Content: Real Estate Brokers Law (1996) and Ethics only.
2. Structure: Case description and 4 options (א, ב, ג, ד).
3. NO explanations or learning content.
4. Language: Hebrew.
Output JSON only:
{
  "question_text": "...",
  "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "correct_idx": int,
  "legal_source": "סעיף חוק"
}
"""

def initialize_exam():
    """אתחול מבנה הנתונים בזיכרון הסשן"""
    if "exam_state" not in st.session_state:
        st.session_state.exam_state = {
            "current_index": -1, # -1 אומר שאנחנו בדף ההסבר
            "questions": [],
            "answers": {},
            "start_time": None,
            "is_finished": False,
            "is_loading": False
        }

def fetch_next_question():
    """מנגנון השרשרת: מייצר שאלה אחת בכל פעם ברקע עד להגעה ל-25"""
    state = st.session_state.exam_state
    
    # תנאי עצירה: אם הגענו ל-25 או שאנחנו כבר בתהליך טעינה
    if len(state['questions']) >= 25 or state.get('is_loading', False):
        return

    state['is_loading'] = True
    try:
        # הגדרת ה-API
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # יצירת התוכן
        response = model.generate_content(EXAM_PROMPT)
        res_text = response.text
        
        # חילוץ ה-JSON מהתשובה
        match = re.search(r'\{.*\}', res_text, re.DOTALL)
        if match:
            q_data = json.loads(match.group())
            
            # בדיקה שהשאלה לא ק
