import google.generativeai as genai
import streamlit as st
import json, re

EXAM_PROMPT = """
As an expert in the Israeli Real Estate Brokers License Exam, generate a "Scenario-Based" question.
FOCUS ONLY on: Real Estate Brokers Law (1996), Ethics Regulations.
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

def fetch_question_to_queue():
    state = st.session_state.exam_state
    if len(state['questions']) < 25:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-2.0-flash')
            res = model.generate_content(EXAM_PROMPT).text
            match = re.search(r'\{.*\}', res, re.DOTALL)
            if match:
                q_data = json.loads(match.group())
                state['questions'].append(q_data)
        except:
            pass
