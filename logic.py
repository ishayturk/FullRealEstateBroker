import google.generativeai as genai
import streamlit as st
import json, re

# פרומפט המבחן המקצועי - מבוסס ניתוח בחינות רשם המתווכים
EXAM_PROMPT = """
As an expert in the Israeli Real Estate Brokers License Exam, generate a "Scenario-Based" question (Case Study).
The question must follow the exact style of the Ministry of Justice exams.

Guidelines:
1. THE SCENARIO: A complex professional situation (e.g., commission dispute, multiple brokers, or legal breach).
2. THE LEGAL CORE: Test knowledge of the Real Estate Brokers Law (1996) or related Regulations.
3. THE DISTRACTORS: Options must be long, detailed, and legally plausible.
4. Only one option must be 100% legally correct.

Output ONLY a JSON:
{
  "question_text": "תיאור המקרה המשפטי והשאלה בסופו...",
  "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "correct_idx": int,
  "legal_source": "סעיף החוק המדויק"
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

def generate_question_sync(index):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(EXAM_PROMPT).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        return {"question_text": "שגיאה בייצור שאלה", "options": ["א","ב","ג","ד"], "correct_idx": 0}
