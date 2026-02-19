import os
import json
import random
import streamlit as st

# הגדרות ליבה (נאמנות לעוגן 1218-G2 ופרוטוקול C-01)
EXAMS_DIR = "exams_data"
FILE_PREFIX = "test_"
FILE_EXTENSION = ".json"
VERSION = "1218-G2"

def load_exam_data(filename):
    """טעינת קובץ JSON מהמאגר"""
    path = os.path.join(EXAMS_DIR, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"שגיאה טכנית בטעינה: {e}")
        return None

def main():
    # הגדרות תצוגה (RTL)
    st.set_page_config(page_title=f"מערכת בחינות {VERSION}", layout="centered")
    
    # CSS ליישור לימין
    st.markdown("""
        <style>
        .main { direction: rtl; text-align: right; }
        div[role="radiogroup"] { direction: rtl; }
        </style>
    """, unsafe_allow_html=True)

    # ניהול מצב סשן בחינה
    if 'exam_started' not in st.session_state:
        st.session_state.exam_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'selected_exam' not in st.session_state:
        st.session_state.selected_exam = None

    # --- שלב דף ההסבר ---
    if not st.session_state.exam_started:
        st.title("📖 בחינת רישום מתווכים")
        st.subheader("הוראות לנבחן")
        
        st.write("""
        1. המבחן כולל 25 שאלות שנבחרו באקראי מהמועד שנבחר.
        2. לא ניתן לחזור אחורה לשאלות קודמות.
        3. יש לסמן תשובה אחת וללחוץ על 'שאלה הבאה'.
        """)
        
        st.divider()
        confirmed = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
        
        if st.button("מעבר לבחינה"):
            if confirmed:
                # איתור קבצים בתיקייה
                if not os.path.exists(EXAMS_DIR):
                    st.error(f"שגיאה: התיקייה {EXAMS_DIR} לא נמצאה.")
                    return
                
                files = sorted([f for f in os.listdir(EXAMS_DIR) if f.startswith(FILE_PREFIX) and f.endswith(FILE_EXTENSION)])
                
                if not files:
                    st.error("לא נמצאו קבצי בחינה תקינים במאגר.")
                    return
                
                # בחירת בחינה (רנדומלית מהמאגר הקיים)
                selected_file = random.choice(files)
                data = load_exam_data(selected_file)
                
                if data and 'questions' in data:
                    all_qs = data['questions']
                    # הגבלה ל-25 שאלות לפי הגדרות המערכת
                    st.session_state.questions = random.sample(all_qs, min(len(all_qs), 25))
                    st.session_state.selected_exam = selected_file
                    st.session_state.exam_started = True
                    st.rerun()
            else:
                st.warning("חובה לאשר את ההוראות לפני תחילת המבחן.")

    # --- שלב הבחינה הפעילה ---
    else:
        idx = st.session_state.current_question
        total = len(st.session_state.questions)

        if idx < total:
            q = st.session_state.questions[idx]
            
            st.write(f"**מבחן:** {st.session_state.selected_exam}")
            st.progress((idx) / total)
            st.subheader(f"שאלה {idx + 1} מתוך {total}")
            
            # הצגת תוכן השאלה (מפתח question_text לפי C-01)
            st.info(q.get('question_text', 'שגיאה בטעינת תוכן השאלה'))

            # הצגת אפשרויות
            options = q.get('options', [])
            st.radio("בחר תשובה:", options, key=f"q_{idx}")

            if st.button("שאלה הבאה"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            # סיום בחינה
            st.balloons()
            st.success("הבחינה הסתיימה בהצלחה!")
            if st.button("חזרה לדף הסבר"):
                # איפוס מלא של הסשן להתחלה מחדש
                st.session_state.exam_started = False
                st.session_state.current_question = 0
                st.session_state.questions = []
                st.rerun()

if __name__ == "__main__":
    main()
