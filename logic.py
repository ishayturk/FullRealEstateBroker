import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

class ExamManager:
    def __init__(self):
        self.data_folder = "exams_data"

    def load_exam(self):
        # מניעת טעינה כפולה באותו סשן
        if 'full_exam_data' in st.session_state and st.session_state.full_exam_data:
            return st.session_state.full_exam_data
            
        try:
            if not os.path.exists(self.data_folder):
                return None
            
            files = [f for f in os.listdir(self.data_folder) if f.lower().endswith('.json')]
            if not files:
                return None
                
            # בחירת מבחן אקראי מהקבצים שהעלית
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                st.session_state.full_exam_data = data
                return data
        except Exception:
            return None
