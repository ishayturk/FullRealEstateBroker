# Project: מתווך בקליק | Version: B02-Fixed
# File: ai_engine.py
import streamlit as st
import google.generativeai as genai
import json, re

def configure_ai():
    """מוצא אוטומטית את המודל שהמפתח שלך מורשה להפעיל"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # רשימת המודלים שאנחנו מעדיפים, לפי סדר עדיפות
        preferred_models = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]
        
        # בדיקה איזה מהם זמין עבור המפתח שלך
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        for model_id in preferred_models:
            # הוספת הקידומת models/ אם היא חסרה ברשימה שגוגל החזיר
            full_id = f"models/{model_id}"
            if full_id in available_models or model_id in available_models:
                return genai.GenerativeModel(model_id)
        
        # אם לא מצאנו מהמועדפים, ניקח את הראשון שזמין בכלל
        if available_models:
            return genai.GenerativeModel(available_models[0].replace('models/', ''))
            
        return None
    except Exception as e:
        print(f"Detailed Auth Error: {e}")
        return None

def fetch_quick_question(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    
    prompt = f"צור שאלת הבנה קצרה בפורמט JSON על {sub_topic} בחוק {topic}. מבנה: {{'q':'', 'options':['','','',''], 'correct':'', 'explain':''}}"
    try:
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        return json.loads(match.group().replace("'", '"')) if match else None
    except:
        return None

def stream_lesson(topic, sub_topic):
    model = configure_ai()
    if not model: return None
    
    prompt = f"כתוב שיעור הכנה למבחן המתווכים על {sub_topic} בחוק {topic}."
    try:
        return model.generate_content(prompt, stream=True)
    except:
        return None
