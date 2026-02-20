import google.generativeai as genai
import streamlit as st
import json, re

# פרומפט בחינה "יבש" בלבד
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
    if "exam_state" not in st.session_state:
        st.session_state.exam_state = {
            "current_index": -1,
            "questions": [],
            "answers": {},
            "start_time": None,
            "is_finished": False,
            "is_loading": False
        }

def fetch_next_question():
    """מנגנון השרשרת: מייצר שאלה אחת ודוחף אותה לתור"""
    state = st.session_state.exam_state
    if len(state['questions']) < 25 and not state.get('is_loading', False):
        state['is_loading'] = True
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-2.0-flash')
            res = model.generate_content(EXAM_PROMPT).text
            match = re.search(r'\{.*\}', res, re.DOTALL)
            if match:
                q_data = json.loads(match.group())
                # מניעת כפילויות בסיסית
                if q_data['question_text'] not in [q['question_text'] for q in state['questions']]:
                    state['questions'].append(q_data)
        except Exception as e:
            pass
        finally:
            state['is_loading'] = False
