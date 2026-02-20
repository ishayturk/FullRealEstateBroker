import google.generativeai as genai
import streamlit as st
import json, re

# פרומפט המבחן המקצועי - ממוקד בחוק המתווכים ואתיקה
EXAM_PROMPT = """
As an expert in the Israeli Real Estate Brokers License Exam, generate a "Scenario-Based" question.
FOCUS ONLY on: Real Estate Brokers Law (1996), Ethics Regulations, and directly related professional topics.
Output ONLY a JSON:
{
  "question_text": "תיאור המקרה המשפטי...",
  "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "correct_idx": int,
  "legal_source": "סעיף החוק"
}
"""

def initialize_exam():
    if "exam_state" not in st.session_state:
        st.session_state.exam_state = {
            "current_index": -1,
            "questions": [],
            "answers": {},
            "start_time": None,
            "is_finished": False
        }

def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel('gemini-2.0-flash')

def fetch_and_store_question():
    """מייצר שאלה ושומר אותה ברשימה בזיכרון"""
    state = st.session_state.exam_state
    if len(state['questions']) < 25:
        try:
            model = get_model()
            res = model.generate_content(EXAM_PROMPT).text
            match = re.search(r'\{.*\}', res, re.DOTALL)
            if match:
                new_q = json.loads(match.group())
                state['questions'].append(new_q)
        except Exception as e:
            state['questions'].append({"question_text": f"שגיאת טעינה: {str(e)}", "options": ["-","-","-","-"], "correct_idx": 0})
