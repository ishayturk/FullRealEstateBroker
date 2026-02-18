import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

class ExamManager:
    def __init__(self, total_questions=25, time_limit=120):
        self.total_questions = total_questions
        self.time_limit = time_limit
        self.data_folder = "exams_data"
        
        if 'questions' not in st.session_state: st.session_state.questions = []
        if 'full_exam_data' not in st.session_state: st.session_state.full_exam_data = None

    def load_exam_from_json(self):
        if st.session_state.full_exam_data is not None:
            return True
        try:
            if not os.path.exists(self.data_folder): return False
            files = [f for f in os.listdir(self.data_folder) if f.lower().endswith('.json')]
            if not files: return False
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            with open(path, 'r', encoding='utf-8') as f:
                st.session_state.full_exam_data = json.load(f)
            return True
        except Exception:
            return False

    def fetch_batch(self, start_idx):
        if not st.session_state.full_exam_data: return
        all_q = st.session_state.full_exam_data.get('questions', [])
        st.session_state.questions.extend(all_q[start_idx : start_idx + 5])
