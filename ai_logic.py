# ai_logic.py | Version: C-01
import streamlit as st
import google.generativeai as genai

def stream_ai_lesson(subtopic):
    """
    מנהל את הקשר מול Gemini ומזרים את השיעור והשאלון.
    """
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = (f"הסבר באופן מקצועי וממוקד למתווכי מקרקעין על: {subtopic}. "
                  f"מיד לאחר ההסבר, הוסף שאלון חזרה מהיר הכולל 10 שאלות אמריקאיות "
                  f"קצרות ונקודתיות שבוחנות את הבנת החומר שנלמד כרגע. "
                  f"בסוף, הצג מפתח תשובות ברור.")
        
        response = model.generate_content(prompt, stream=True)
        return response
    except Exception as e:
        st.error(f"שגיאה בתקשורת עם ה-AI: {e}")
        return None
