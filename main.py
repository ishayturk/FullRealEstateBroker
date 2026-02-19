import streamlit as st
import json
import os
import random

# הגדרות עמוד בסיסיות
st.set_page_config(page_title="מבחן מתווכים", layout="wide", initial_sidebar_state="collapsed")

# הזרקת CSS ליישור לימין (RTL) ועיצוב נקי
st.markdown("""
    <style>
    /* הגדרת כיווניות כללית */
    .stApp {
        direction: RTL;
        text-align: right;
    }
    /* יישור טקסט וכותרות */
    h1, h2, h3, p, label, div {
        text-align: right !important;
        direction: RTL !important;
    }
    /* עיצוב הצ'קבוקס עם הפרדה מהתיאור */
    .stCheckbox {
        margin-top: 30px;
        margin-bottom: 20px;
        gap: 15px;
    }
    /* כפתור מעבר לבחינה */
    div.stButton > button {
        width: 220px;
        height: 50px;
        font-weight: bold;
    }
    /* הסתרת רכיבי Sidebar כשהוא סגור */
    [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

def get_random_exam():
    """בוחר קובץ מבחן אקראי שלא נעשה בסשן הנוכחי"""
    all_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    # סינון מבחנים שכבר נעשו בסשן הזה
    if 'completed_exams' not in st.session_state:
        st.session_state.completed_exams = []
        
    available_files = [f for f in all_files if f not in st.session_state.completed_exams]
    
    # אם עברנו על הכל, נאפס את הרשימה (כדי לא להיתקע)
    if not available_files:
        available_files = all_files
        st.session_state.completed_exams = []
        
    return random.choice(available_files) if available_files else None

def load_batch(start_idx, count=5):
    """טוענת מנה של שאלות לתוך הזיכרון המצטבר"""
    if 'full_exam_data' in st.session_state:
        questions = st.session_state.full_exam_data
        end_idx = min(start_idx + count, len(questions))
        new_questions = questions[start_idx:end_idx]
        
        # הוספה לזיכרון המצטבר
        st.session_state.loaded_questions.extend(new_questions)

def main():
    # אתחול משתני מערכת (מבוצע פעם אחת בטעינה ראשונה של הפריים)
    if 'initialized' not in st.session_state:
        st.session_state.page = 'explanation'
        st.session_state.current_q_idx = 0
        st.session_state.user_answers = {}
        st.session_state.loaded_questions = []
        st.session_state.submitted = False
        
        # טריגר מיידי: בחירת מבחן וטעינת 5 שאלות ראשונות "באוויר"
        selected_file = get_
