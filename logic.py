import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G2
# לוגיקה לטעינת מבחנים מתיקיית הנתונים שהוגדרה בריפוזיטורי

class ExamManager:
    def __init__(self, total_questions=25, time_limit=120):
        self.total_questions = total_questions
        self.time_limit = time_limit
        self.data_folder = "exams_data"
        
        # אתחול Session State למניעת טעינה כפולה
        if 'questions' not in st.session_state: st.session_state.questions = []
        if 'answers' not in st.session_state: st.session_state.answers = {}
        if 'full_exam_data' not in st.session_state: st.session_state.full_exam_data = None

    def load_exam_from_json(self):
        """טוען מבחן אקראי מתוך התיקייה בריפוזיטורי"""
        if st.session_state.full_exam_data is not None:
            return True
            
        try:
            if not os.path.exists(self.data_folder):
                st.error(f"התיקייה {self.data_folder} לא נמצאה ב-Root.")
                return False

            # רשימת קבצים שמתחילים ב-test (תומך בכל סיומת json/JSON)
            files = [f for f in os.listdir(self.data_folder) 
                     if f.startswith('test') and f.lower().endswith('.json')]
            
            if not files:
                st.error("לא נמצאו קבצי מבחן בתיקייה.")
                return False
            
            # בחירה רנדומלית של מבחן לסשן הנוכחי
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            
            with open(path, 'r', encoding='utf-8') as f:
                st.session_state.full_exam_data = json.load(f)
            return True
        except Exception as e:
            st.error(f"שגיאה קריטית בטעינת נתוני הבחינה: {e}")
            return False

    def fetch_batch(self, start_idx):
        """טעינת מנות של 5 שאלות (לוגיקת 5-5-5)"""
        if not st.session_state.full_exam_data:
            return
            
        all_questions = st.session_state.full_exam_data.get('questions', [])
        new_batch = all_questions[start_idx : start_idx + 5]
        st.session_state.questions.extend(new_batch)
