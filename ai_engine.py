# Project: מתווך בקליק | Version: B01
# File: ai_engine.py
import streamlit as st
import google.generativeai as genai
import json, re

def configure_ai():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel('gemini-2.0-flash')

def fetch_quick_question(topic, sub_topic):
    """מייצר שאלה קצרה ומהירה לבדיקת הבנה (בזק)"""
    model = configure_ai()
    prompt = f"""
    צור שאלת הבנה קצרה מאוד על {sub_topic} (בתוך חוק {topic}).
    השאלה והתשובות חייבות להיות תמציתיות (משפט אחד).
    החזר אך ורק JSON:
    {{
      'q': 'השאלה הקצרה',
      'options': ['א', 'ב', 'ג', 'ד'],
      'correct': 'התשובה המדויקת',
      'explain': 'הסבר של שורה אחת'
    }}
    """
    try:
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def fetch_exam_question(topic):
    """מייצר שאלה ברמת מבחן (ארוכה ומורכבת)"""
    model = configure_ai()
    # בשלב זה AI מייצר, בשלב הבא נחבר למאגר הקבצים שלך
    prompt = f"צור שאלה אמריקאית מורכבת וארוכה בסגנון מבחן המתווכים על {topic}. החזר JSON בלבד."
    try:
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None

def stream_lesson(topic, sub_topic):
    """מזרים את תוכן השיעור למסך"""
    model = configure_ai()
    prompt = f"כתוב שיעור הכנה מעמיק למבחן המתווכים על {sub_topic} בחוק {topic}. פרט סעיפי חוק ודוגמאות. ללא כותרות."
    try:
        return model.generate_content(prompt, stream=True)
    except:
        return None
