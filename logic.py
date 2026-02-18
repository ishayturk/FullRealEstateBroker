import streamlit as st
import json
import os
import random
import re

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

class ExamManager:
    def __init__(self):
        self.data_folder = "exams_data"

    def load_exam(self):
        if 'full_exam_data' in st.session_state and st.session_state.full_exam_data:
            return st.session_state.full_exam_data
            
        try:
            if not os.path.exists(self.data_folder):
                return None
            
            files = [f for f in os.listdir(self.data_folder) if f.lower().endswith('.json')]
            if not files:
                return None
                
            chosen_file = random.choice(files)
            path = os.path.join(self.data_folder, chosen_file)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # ניקוי תווים לא חוקיים שעלולים להיווצר בהעתקה/הדבקה (כמו שורות חדשות בתוך גרשיים)
                # מחליף תווים לבנים לא חוקיים ברווח רגיל
                clean_content = re.sub(r'[\x00-\x1F\x7F]', ' ', content)
                
                data = json.loads(clean_content, strict=False)
                
                if 'questions' in data:
                    st.session_state.full_exam_data = data
                    st.session_state.current_filename = chosen_file 
                    return data
                return None
        except Exception as e:
            st.error(f"שגיאת קריאה בקובץ {chosen_file}: וודא שהפורמט תקין.")
            return None
