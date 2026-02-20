import google.generativeai as genai
import streamlit as st
import json, re

# פרומפט המבחן המקצועי - ממוקד בחוק המתווכים ובאתיקה בלבד
EXAM_PROMPT = """
As an expert in the Israeli Real Estate Brokers License Exam, generate a "Scenario-Based" question.
FOCUS ONLY on: Real Estate Brokers Law (1996), Ethics Regulations, and directly related professional topics.
DO NOT include general law questions or non-brokerage legal topics.

Guidelines:
1. THE SCENARIO: A professional case involving a broker, client, and a property transaction.
2. LEGAL BASIS: The question must test specific clauses of the Brokers Law or Ethics.
3. THE DISTRACTORS: Options must be legally plausible and professional.
4. CORRECT OPTION: Only one option is 100% correct according to the law.

Output ONLY a JSON:
{
  "question_text": "תיאור המקרה המשפטי הממוקד במתווכים...",
  "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "correct_idx": int,
  "legal_source": "סעיף החוק הרלוונטי"
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
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        res = model.generate_content(EXAM_PROMPT).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        return {"question_text": "שגיאה בייצור שאלה", "options": ["-","-","-","-"], "correct_idx": 0}
    except Exception as e:
        return {"question_text": f"שגיאת תקשורת: {str(e)}", "options": ["-","-","-","-"], "correct_idx": 0}
