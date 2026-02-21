# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: logic_v06 | Date: 21/02/2026 | 23:35
import streamlit as st
import time

def initialize_exam():
    """אתחול משתני המערכת בזיכרון"""
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
        st.session_state.current_q = 1
        st.session_state.start_time = None
        st.session_state.answers_user = {}
        # טעינה מוקדמת של שאלה ראשונה
        generate_question(1)

def generate_question(q_number):
    """ייצור שאלה מקצועית על בסיס חוק המתווכים"""
    # בנק שאלות לדוגמה - רמה מקצועית
    real_questions = {
        1: {
            "question": "על פי חוק המתווכים, מהו התנאי לזכאות לדמי תיווך?",
            "options": [
                "רישיון בתוקף, הזמנה בכתב והיות המתווך הגורם היעיל",
                "חתימה על הסכם בלעדיות בלבד",
                "הצגת הנכס ללקוח ללא צורך במסמכים נוספים",
                "רישום המתווך באיגוד המתווכים הארצי"
            ],
            "correct": 0
        },
        2: {
            "question": "מהו תקופת הבלעדיות המרבית בדירת מגורים?",
            "options": [
                "3 חודשים",
                "6 חודשים",
                "9 חודשים",
                "שנה אחת"
            ],
            "correct": 1
        }
    }
    
    if q_number in real_questions:
        st.session_state.exam_data[q_number] = real_questions[q_number]
    else:
        # יצירת מבנה לשאלות עתידיות (3-25)
        st.session_state.exam_data[q_number] = {
            "question": f"שאלה מקצועית {q_number}: בעניין חוק המקרקעין...",
            "options": ["אופציה א'", "אופציה ב'", "אופציה ג'", "אופציה ד'"],
            "correct": 0
        }

def handle_navigation(direction):
    """ניהול מעברים ולוגיקת n+2"""
    curr = st.session_state.current_q
    if direction == "next":
        target = curr + 1
        n_load = target + 1
        if n_load <= 25 and n_load not in st.session_state.exam_data:
            generate_question(n_load)
        st.session_state.current_q = target
    elif direction == "prev" and curr > 1:
        st.session_state.current_q -= 1

def get_timer_display():
    """חישוב זמן נותר"""
    if st.session_state.start_time is None:
        return "90:00"
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(rem), 60)
    return f"{mins:02d}:{secs:02d}"

def check_exam_status():
    """בדיקה אם הזמן הסתיים"""
    if st.session_state.start_time is None:
        return False
    return (time.time() - st.session_state.start_time) >= (90 * 60)

def get_results_data():
    """חישוב ציון ונתוני משוב"""
    results = []
    score = 0
    for i in range(1, 26):
        q = st.session_state.exam_data.get(i)
        ans = st.session_state.answers_user.get(i)
        is_correct = (q and ans is not None and ans == q["correct"])
        if is_correct:
            score += 4
        
        results.append({
            "num": i,
            "is_correct": is_correct,
            "user_text": q["options"][ans] if (q and ans is not None) 
                         else "לא נענתה",
            "correct_text": q["options"][q["correct"]] if q else "N/A"
        })
    return score, results

# סוף קובץ
