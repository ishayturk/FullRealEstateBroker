import google.generativeai as genai
import streamlit as st
import json, re

# פרומפט מקצועי - ממוקד בחוק המתווכים ואתיקה
EXAM_PROMPT = """
As an expert in the Israeli Real Estate Brokers License Exam, generate a "Scenario-Based" question.
FOCUS ONLY on: Real Estate Brokers Law (1996), Ethics Regulations, and directly related professional topics.
DO NOT include general law questions or non-brokerage legal topics.

Output ONLY a JSON:
{
  "question_text": "תיאור המקרה המשפטי...",
  "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "correct_idx": int,
  "legal_source": "סעיף החוק הרלוונטי"
}
"""

def initialize_exam():
    if "exam_state" not in st.session_state:
        st.session_state.exam_state = {
            "current_index": -1,
            "questions": [], # רשימת השאלות שנוצרו
            "answers": {},
            "start_time": None,
            "is_finished": False
        }

def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel('gemini-2.0-flash')

def fetch_next_question_if_needed():
    """
    מנהל את ה-Prefetching: 
    מייצר את השאלה הבאה בתור אם היא עדיין לא קיימת בזיכרון (עד 25 שאלות).
    """
    state = st.session_state.exam_state
    # אם חסרה שאלה בתור (למשל כרגע בשאלה 2 ויש רק 2 שאלות בזיכרון)
    if len(state['questions']) < 25 and len(state['questions']) <= state['current_index'] + 1:
        try:
            model = get_model()
            res = model.generate_content(EXAM_PROMPT).text
            match = re.search(r'\{.*\}', res, re.DOTALL)
            if match:
                new_q = json.loads(match.group())
                state['questions'].append(new_q)
        except Exception as e:
            # הכנסת שאלת "תקלה" כדי לא לתקוע את התור
            state['questions'].append({
                "question_text": f"שגיאת טעינה זמנית: {str(e)}", 
                "options": ["-","-","-","-"], 
                "correct_idx": 0
            })
