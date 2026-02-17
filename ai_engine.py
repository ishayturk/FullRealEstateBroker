# Project: מתווך בקליק | Version: B03
# File: ai_engine.py
import streamlit as st
import google.generativeai as genai
import json, re

def configure_ai():
    """הגדרה למודל Gemini 2.0 Flash בלבד"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # שימוש בשם המודל המדויק
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"שגיאת קונפיגורציה: {e}")
        return None

def stream_lesson(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    
    prompt = f"""
    אתה מרצה מומחה לנדל"ן בישראל. 
    כתוב שיעור הכנה מפורט למבחן המתווכים על: {sub_topic} (במסגרת {topic}).
    השתמש בסעיפי חוק רלוונטיים, הסבר בשפה ברורה, והוסף דוגמה מעשית אחת לפחות.
    אל תכתוב כותרות ראשיות, התחל ישר בתוכן.
    """
    try:
        return model.generate_content(prompt, stream=True)
    except Exception as e:
        st.error(f"שגיאת AI: {e}")
        return None

def fetch_quick_question(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    
    prompt = f"""
    צור שאלת אמריקאית אחת על {sub_topic}.
    החזר אך ורק JSON במבנה הזה:
    {{
      "q": "השאלה",
      "options": ["א", "ב", "ג", "ד"],
      "correct": "התשובה המדויקת",
      "explain": "הסבר קצר"
    }}
    """
    try:
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match:
            return json.loads(match.group().replace("'", '"'))
        return None
    except:
        return None
