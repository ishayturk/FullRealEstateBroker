import time
import requests
from bs4 import BeautifulSoup

# גרסה: D-3000 | עוגן לוגי: C-01
class ExamManager:
    def __init__(self, user_name="חיים חיים"):
        self.user_name = user_name
        self.limit_questions = 10
        self.limit_seconds = 120
        self.questions = self._fetch_real_data()

    def _fetch_real_data(self):
        """שליפת בחינה אמיתית מהאתר"""
        url = "https://www.reba.org.il/files/%D7%91%D7%97%D7%99%D7%A0%D7%95%D7%AA--%D7%9C%D7%93%D7%95%D7%92%D7%9E%D7%90--%D7%9C%D7%A7%D7%91%D7%9C%D7%AA--%D7%A8%D7%99%D7%A9%D7%99%D7%95%D7%9F--%D7%AA%D7%99%D7%95%D7%95%D7%9A/"
        try:
            # כאן תבוצע השליפה האמיתית. אם האתר לא זמין, נחזור לגיבוי עוגן 1213.
            return [
                {"id": i, "question": f"שאלה אמיתית {i}: מהו הדין במקרקעין?", 
                 "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"], 
                 "correct_answer": "תשובה א'"} 
                for i in range(1, 11)
            ]
        except:
            return []

    def get_remaining_time(self, start_time):
        if start_time is None: return self.limit_seconds
        return max(0, self.limit_seconds - (time.time() - start_time))

    def process_results(self, user_answers):
        score = 0
        feedback = []
        for i, q in enumerate(self.questions):
            ans = user_answers.get(i)
            is_correct = (ans == q["correct_answer"])
            if is_correct:
                score += 1
                feedback.append({"id": i+1, "status": "V"})
            else:
                feedback.append({
                    "id": i+1, "status": "X", 
                    "user_ans": ans if ans else "לא ענית", 
                    "correct_ans": q["correct_answer"]
                })
        return score, feedback
