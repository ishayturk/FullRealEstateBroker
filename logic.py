import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

class ExamManager:
    def __init__(self):
        self.data_folder = "exams_data"
        if 'full_exam_data' not in st.session_state: 
            st.session_state.full_exam_data = None

    def load_exam(self):
        # אם כבר טענו מבחן בסשן הזה, אל תטען שוב (מונע כפילויות)
        if st.session_state.full_exam_data:
            return st.session_state.full_exam_data
            
        try:
            if not os.path.exists(self.data_folder):
                return None
            files = [f for f in os.listdir(self.data_folder) if f.endswith('.json')]
            if not files:
                return None
                
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            with open(path, 'r', encoding='utf-8') as f:
                st.session_state.full_exam_data = json.load(f)
            return st.session_state.full_exam_data
        except:
            return None
