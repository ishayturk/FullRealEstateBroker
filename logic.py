# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2

import os
import json
import random
import streamlit as st

class ExamLogic:
    def __init__(self, data_folder='exams_data'):
        self.data_folder = data_folder
        self.total_seconds = 7200  # שעתיים

    def get_available_exams(self):
        """סורק את התיקייה ומחזיר רשימת שמות קבצי JSON"""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        return [f for f in os.listdir(self.data_folder) if f.endswith('.json')]

    def load_exam(self, filename):
        """טוען מבחן ספציפי מהתיקייה"""
        path = os.path.join(self.data_folder, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def select_next_exam(self, used_exams):
        """בוחר מבחן חדש שלא נעשה בסשן"""
        all_exams = self.get_available_exams()
        available = [e for e in all_exams if e not in used_exams]
        
        if not available:
            # אם סיימנו את כל המאגר, נאפשר להתחיל מחדש
            available = all_exams
            used_exams.clear()
            
        selected = random.choice(available)
        return selected, self.load_exam(selected)

    def format_time(self, seconds_left):
        mins, secs = divmod(seconds_left, 60)
        hrs, mins = divmod(mins, 60)
        return f"{hrs:02}:{mins:02}:{secs:02}"
