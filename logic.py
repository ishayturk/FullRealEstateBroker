import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G7
# לוגיקה לטעינת מבחנים רנדומליים מתיקיית exams_data

class ExamManager:
    def __init__(self, total_questions=25, time_limit=120):
        self.total_questions = total_questions
        self.time_limit = time_limit
        self.data_folder = "exams_data"
        
        if 'questions' not in st.session_state: st.session_state.questions = []
        if 'answers' not in st.session_state: st.session_state.answers = {}
        if 'full_exam_data' not in st.session_state: st.session_state.full_exam_data = None

    def load_exam_from_json(self):
        """טעינת קובץ JSON אקראי מהתיקייה (עוגן 1217)"""
        if st.session_state.full_exam_data is not None:
            return True
        try:
            if not os.path.exists(self.data_folder):
                st.error(f"Missing folder: {self.data_folder}")
                return False

            files = [f for f in os.listdir(self.data_folder) if f.endswith('.json')]
            if not files:
                st.error("No JSON exam files found.")
                return False
            
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            
            with open(path, 'r', encoding='utf-8') as f:
                st.session_state.full_exam_data = json.load(f)
            return True
        except Exception as e:
            st.error(f"Error loading exam data: {e}")
            return False

    def fetch_batch(self, start_idx):
        """מימוש לוגיקת 5-5-5"""
        if not st.session_state.full_exam_data:
            return
        all_q = st.session_state.full_exam_data.get('questions', [])
        st.session_state.questions.extend(all_q[start_idx : start_idx + 5])
