import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

class ExamManager:
    def __init__(self):
        self.data_folder = "exams_data"
        # וידוא שקיים נתיב לתיקייה
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def load_exam(self):
        # לוגיקה: לא להטעין פעמיים באותו סשן (מניעת כפילות)
        if 'full_exam_data' in st.session_state and st.session_state.full_exam_data:
            return st.session_state.full_exam_data
            
        try:
            # קריאת כל הקבצים
            files = [f for f in os.listdir(self.data_folder) if f.lower().endswith('.json')]
            
            if not files:
                return None
                
            # בחירת קובץ אקראי
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                st.session_state.full_exam_data = data
                return data
        except Exception as e:
            return None
