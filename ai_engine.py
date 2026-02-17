import streamlit as st
import google.generativeai as genai
import json, re

def configure_ai():
    """הגדרה קשיחה ל-Gemini 2.0 Flash"""
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("המפתח GEMINI_API_KEY חסר ב-Secrets!")
            return None
            
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # שם המודל המדויק לגרסת ה-2.0 היציבה
        # אם זה עדיין נכשל, ננסה להוסיף 'models/' לפני השם
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        st.error(f"שגיאת Gemini 2.0: {e}")
        return None

def stream_lesson(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    
    # הוספת הנחיה למודל 2.0 להיות ממוקד
    prompt = f"אתה מורה לנדל\"ן. כתוב שיעור הכנה למבחן המתווכים על {sub_topic} (חוק {topic}). פרט סעיפים חשובים."
    try:
        # בגרסה 2.0 ה-streaming עובד מצוין
        return model.generate_content(prompt, stream=True)
    except Exception as e:
        st.error(f"שגיאה בהזרמת תוכן 2.0: {e}")
        return None

def fetch_quick_question(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    
    prompt = f"צור שאלת JSON על {sub_topic}. מבנה: {{'q':'', 'options':['','','',''], 'correct':'', 'explain':''}}"
    try:
        # מודל 2.0 מעולה ב-JSON, ננצל את זה
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match:
            clean_json = match.group().replace("'", '"')
            return json.loads(clean_json)
        return None
    except:
        return None
