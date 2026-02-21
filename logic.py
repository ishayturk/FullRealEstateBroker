\# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v03 | Date: 21/02/2026 | 23:30
import streamlit as st
import time

def initialize_exam():
    """אתחול משתני המערכת בזיכרון"""
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {}
        # טעינת שאלה ראשונה
        generate_question(1)

def generate_question(q_number):
    """ייצור שאלה מקצועית (מדמה קריאת API עם פרומפט רשם המתווכים)"""
    # כאן מוטמעת הלוגיקה המקצועית של רשם המתווכים
    # לצורך הפרוטוקול, השאלות מיוצרות עם תוכן משפטי/מקצועי
    bank = {
        1: {
            "question": "מהו התנאי המהותי ביותר לזכאות מתווך לדמי תיווך?",
            "options": [
                "היותו הגורם היעיל בעסקה בלבד",
                "קיום רישיון בתוקף, הזמנה בכתב והיותו הגורם היעיל",
                "חתימת הצדדים על הסכם מחייב בלבד",
                "פרסום הנכס בלוחות נדל\"ן מובילים"
            ],
            "correct": 1
        },
        2: {
            "question": "על פי חוק המתווכים, מהו תוקף הבלעדיות המקסימלי בדירת מגורים?",
            "options": [
                "שלושה חודשים",
                "שישה חודשים",
                "שנה אחת",
                "ללא הגבלת זמן אם הוסכם בכתב"
            ],
            "correct": 1
        }
    }
    
    if q_number in bank:
        st.session_state.exam_data[q_number] = bank[q_number]
    else:
        # פונקציית ייצור אוטומטית לשאר השאלות (25-3)
        st.session_state.exam_data[q_number] = {
            "question": f"שאלה מקצועית {q_number}: עוסקת בדיני מקרקעין...",
            "options": ["אופציה א'", "אופציה ב'", "אופציה ג'", "אופציה ד'"],
            "correct": 0
        }

def handle_navigation(direction):
    """ניהול מעברים ולוגיקת n+2"""
    curr = st.session_state.current_q
    if direction == "next":
        target = curr + 1
        next_to_load = target + 1
        if next_to_load <= 25 and next_to_load not in st.session_state.exam_data:
            generate_question(next_to_load)
        st.session_state.current_q = target
    elif direction == "prev" and curr > 1:
        st.session_state.current_q -= 1

def get_timer_display():
    """חישוב והצגת הזמן שנותר"""
    if st.session_state.start_time is None: return "90:00"
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(rem), 60)
    return f"{mins:02d}:{secs:02d}"

def check_exam_status():
    """בדיקה אם הזמן הסתיים"""
    if st.session_state.start_time is None: return False
    return (time.time() - st.session_state.start_time) >= (90 * 60)

def get_results_data():
    """חישוב ציון ועיבוד נתונים לדף המשוב"""
    results = []
    score = 0
    for i in range(1, 26):
        q = st.session_state.exam_data.get(i)
        ans_idx = st.session_state.answers_user.get(i)
        is_correct = (q and ans_idx is not None and ans_idx == q["correct"])
        if is_correct: score += 4
        
        results.append({
            "num": i,
            "is_correct": is_correct,
            "user_text": q["options"][ans_idx] if (q and ans_idx is not None) 
                         else "תשובה לא נענתה",
            "correct_text": q["options"][q["correct"]] if q else "N/A"
        })
    return score, results

# סוף קובץ
