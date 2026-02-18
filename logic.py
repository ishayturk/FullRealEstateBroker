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
        """טעינת 5 שאלות עם תוכן מלא ברקע"""
        new_batch = []
        # סימולציה של שאלות אמיתיות מאיגוד המתווכים
        data = [
            {"q": "מהו התנאי לקבלת רישיון תיווך?", "o": ["אזרח ישראל", "מעל גיל 18", "ללא עבר פלילי", "כל התשובות נכונות"], "a": "כל התשובות נכונות"},
            {"q": "חוק הגנת הצרכן חל על מתווך?", "o": ["כן", "לא", "רק בעסקאות מעל מיליון שח", "רק בדירות יד שנייה"], "a": "כן"},
            {"q": "מהי תקופת הבלעדיות המקסימלית בדירה?", "o": ["3 חודשים", "6 חודשים", "שנה", "חודש"], "a": "6 חודשים"},
            {"q": "האם מתווך יכול להיות צד בעסקה?", "o": ["כן, תמיד", "לא, אלא אם גילה זאת בכתב", "רק אם הוא לא לוקח עמלה", "אף פעם לא"], "a": "לא, אלא אם גילה זאת בכתב"},
            {"q": "מי רשאי לעסוק בתיווך?", "o": ["מי שיש לו רישיון", "כל אזרח", "עורך דין בלבד", "סטודנט למשפטים"], "a": "מי שיש לו רישיון"}
        ]
        
        for i, item in enumerate(data):
            q_id = start_idx + i + 1
            if q_id <= self.total_questions:
                new_batch.append({
                    "id": q_id,
                    "question": item["q"],
                    "options": item["o"],
                    "correct": item["a"]
                })
        st.session_state.questions.extend(new_batch)

    def start_exam(self):
        st.session_state.start_time = time.time()
        st.session_state.exam_started = True
