import streamlit as st
import google.generativeai as genai
import json, re

def configure_ai():
    try:
        # בדיקה אם המפתח קיים בכלל
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("שגיאה: המפתח GEMINI_API_KEY לא נמצא ב-Secrets!")
            return None
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # נסה להשתמש ב-1.5 פלאש שהוא הכי יציב כרגע
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"שגיאת התחברות לגוגל: {e}")
        return None

def stream_lesson(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    try:
        prompt = f"כתוב שיעור קצר על {sub_topic} בחוק {topic}."
        return model.generate_content(prompt, stream=True)
    except Exception as e:
        st.error(f"שגיאה בייצור תוכן: {e}")
        return None

def fetch_quick_question(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    try:
        prompt = f"צור שאלת JSON על {sub_topic}. מבנה: {{'q':'', 'options':['','','',''], 'correct':'', 'explain':''}}"
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        return json.loads(match.group().replace("'", '"')) if match else None
    except: return None
