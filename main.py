# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v01_foundation | Date: 22/02/2026 | 00:50
import streamlit as st
import time

def initialize_exam():
    """אתחול משתני המערכת בזיכרון (Session State)"""
    if "exam_data" not in st.session_state:
        # מאגר השאלות: מפתח הוא מספר השאלה, הערך הוא מילון נתונים
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {} # שמירת תשובות המשתמש
        
        # טעינה מוקדמת של שאלה 1 כבר בכניסה לעמוד ההסבר
        if 1 not in st.session_state.exam_data:
            generate_question(1)

def generate_question(q_number):
    """ייצור שאלה באמצעות הפרומפט המקצועי (מדמה קריאה ל-LLM)"""
    # כאן יוטמע ה-Prompt המלא של רשם המתווכים
    # המערכת מייצרת שאלה הכוללת: טקסט, 4 תשובות, ומפתח תשובה נכונה.
    
    # סימולציית ייצור (תועבר ל-API בשלב הבא)
    prompt_context = """
    אתה רשם המתווכים. עליך לייצר שאלה מורכבת וברמה גבוהה למבחן הרישוי.
    השאלה חייבת להיות מבוססת על חוק המתווכים, חוק המקרקעין או תקנות רלוונטיות.
    מבנה: שאלה, 4 אפשרויות, תשובה נכונה אחת בלבד.
    """
    
    # לצורך הדגמה ראשונית של המבנה:
    dummy_q = {
        "question": f"שאלה מספר {q_number}: מהו הדין לגבי...",
        "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"],
        "correct": 0 # אינדקס התשובה הנכונה
    }
    
    st.session_state.exam_data[q_number] = dummy_q

def handle_navigation(direction):
    """ניהול לוגיקת המעברים והטעינה המוקדמת (n+2)"""
    curr = st.session_state.current_q
    
    if direction == "next":
        target = curr + 1
        # לוגיקת n+2: אם עברנו ל-target, נכין את target + 1 (שהיא curr + 2)
        next_to_load = target + 1
        if next_to_load <= 25 and next_to_load not in st.session_state.exam_data:
            generate_question(next_to_load)
        
        st.session_state.current_q = target
        
    elif direction == "prev":
        if curr > 1:
            st.session_state.current_q -= 1

def get_timer_display():
    """חישוב הזמן הנותר לטיימר"""
    if st.session_state.start_time is None:
        return "90:00"
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, (90 * 60) - elapsed)
    
    mins, secs = divmod(int(remaining), 60)
    return f"{mins:02d}:{secs:02d}"

def check_exam_status():
    """בדיקה אם הזמן הסתיים"""
    if st.session_state.start_time is None:
        return False
    
    elapsed = time.time() - st.session_state.start_time
    if elapsed >= (90 * 60):
        return True
    return False

# סוף קובץ
