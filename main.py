import streamlit as st
import json
import os
import random

# הגדרות דף
st.set_page_config(page_title="מערכת בחינה - רשם המתווכים", layout="centered")

def get_random_exam():
    data_folder = 'exams_data'
    if not os.path.exists(data_folder):
        return None
    
    # רשימת קבצים תקינים בלבד
    json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
    
    # סינון מבחנים שכבר נעשו בסשן הנוכחי
    if 'played_exams' not in st.session_state:
        st.session_state.played_exams = []
    
    available_files = [f for f in json_files if f not in st.session_state.played_exams]
    
    # אם סיימנו את כל המבחנים, נאפס את הרשימה כדי להתחיל מחדש
    if not available_files:
        available_files = json_files
        st.session_state.played_exams = []

    if available_files:
        chosen_file = random.choice(available_files)
        st.session_state.played_exams.append(chosen_file)
        
        file_path = os.path.join(data_folder, chosen_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

# אתחול Session State
if 'page' not in st.session_state:
    st.session_state.page = 'instructions'
if 'current_exam' not in st.session_state:
    st.session_state.current_exam = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- עמוד 1: הוראות והסברים ---
if st.session_state.page == 'instructions':
    st.title("📋 הוראות לנבחן/ת")
    st.write("""
    1. **משך הבחינה:** שעתיים (120 דקות).
    2. **מבנה הבחינה:** 25 שאלות אמריקאיות.
    3. **ניקוד:** כל שאלה מזכה ב-4 נקודות.
    4. **מעבר:** ציון עובר הוא 60 ומעלה.
    
    בזמן שתלחץ על הכפתור למטה, המערכת תגריל עבורך מבחן ותכין את השאלות.
    """)
    
    if st.button("התחל בחינה והגרל מבחן 🎲"):
        # הגרלה והכנה ברקע
        exam = get_random_exam()
        if exam:
            st.session_state.current_exam = exam
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.page = 'exam'
            st.rerun()
        else:
            st.error("שגיאה בהגרלת המבחן. וודא שיש קבצים תקינים בתיקייה.")

# --- עמוד 2: הבחינה עצמה ---
elif st.session_state.page == 'exam':
    exam = st.session_state.current_exam
    st.title(exam.get('exam_name', 'בחינה'))
    
    for q in exam['questions']:
        st.write(f"**שאלה {q['question_number']}**")
        st.write(q['question_text'])
        
        user_choice = st.radio(
            "בחר תשובה:",
            q['options'],
            key=f"q_{q['question_number']}",
            index=None,
            disabled=st.session_state.submitted
        )
        
        if user_choice:
            st.session_state.answers[q['question_number']] = user_choice[0]

    st.divider()

    if not st.session_state.submitted:
        if st.button("הגש בחינה"):
            st.session_state.submitted = True
            st.rerun()
    else:
        # הצגת תוצאות
        correct = 0
        for q in exam['questions']:
            u_ans = st.session_state.answers.get(q['question_number'])
            c_ans = q['correct_answer']
            if u_ans == c_ans:
                correct += 1
                st.success(f"שאלה {q['question_number']}: נכון")
            else:
                st.error(f"שאלה {q['question_number']}: טעות (נכון: {c_ans})")
        
        st.balloons()
        st.metric("ציון סופי", f"{(correct/len(exam['questions']))*100:.0f}%")
        
        if st.button("חזור למסך הראשי"):
            st.session_state.page = 'instructions'
            st.session_state.current_exam = None
            st.rerun()
