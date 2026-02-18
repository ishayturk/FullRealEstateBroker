import streamlit as st
import json
import os
import random

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

class ExamManager:
    def __init__(self):
        self.data_folder = "exams_data"

    def load_exam(self):
        if 'full_exam_data' in st.session_state and st.session_state.full_exam_data:
            return st.session_state.full_exam_data
            
        try:
            # בדיקה אם התיקייה קיימת
            if not os.path.exists(self.data_folder):
                st.error(f"התיקייה {self.data_folder} לא נמצאה בשרת.")
                return None
            
            # סריקת קבצים
            files = [f for f in os.listdir(self.data_folder) if f.lower().endswith('.json')]
            
            # בדיקת 'דיבאג' שתראה לנו כמה קבצים יש
            if not files:
                st.error("לא נמצאו קבצי JSON בתיקייה exams_data.")
                return None
                
            # בחירה אקראית
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if 'questions' in data:
                    st.session_state.full_exam_data = data
                    # נשמור גם את שם הקובץ לביקורת
                    st.session_state.current_filename = chosen_file 
                    return data
                else:
                    st.error(f"הקובץ {chosen_file} לא מכיל מפתח 'questions'.")
                    return None
        except Exception as e:
            st.error(f"שגיאה בטעינת המבחן: {str(e)}")
            return None
