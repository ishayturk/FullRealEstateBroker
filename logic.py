import streamlit as st
import time

class ExamManager:
    def __init__(self, total_questions=10, time_limit=120):
        self.total_questions = total_questions
        self.time_limit = time_limit
        
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        if 'current_idx' not in st.session_state:
            st.session_state.current_idx = 0
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None

    def fetch_questions_batch(self, start_idx):
        """סימולציה של שליפת 5 שאלות ברקע מאיגוד המתווכים"""
        # כאן תבוא הפונקציה שמושכת מה-URL האמיתי
        new_batch = []
        for i in range(start_idx, start_idx + 5):
            if i < self.total_questions:
                new_batch.append({
                    "id": i + 1,
                    "question": f"שאלה מספר {i + 1} מהמאגר הרשמי?",
                    "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"],
                    "correct": "תשובה א'"
                })
        st.session_state.questions.extend(new_batch)

    def start_exam(self):
        st.session_state.start_time = time.time()
        st.session_state.exam_started = True

    def is_time_up(self):
        if st.session_state.start_time is None:
            return False
        elapsed = time.time() - st.session_state.start_time
        return elapsed >= self.time_limit
