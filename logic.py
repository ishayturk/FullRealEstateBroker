import time

# גרסה: D-3000 | עוגן לוגי: C-01
class ExamManager:
    def __init__(self, user_name="חיים חיים"):
        """
        Constructor (בנאי) - מאתחל את כל נתוני הבחינה
        """
        self.user_name = user_name
        self.limit_questions = 10
        self.limit_seconds = 120  # ה"עוגן" של ה-2 דקות
        self.questions = self._fetch_real_data()

    def _fetch_real_data(self):
        """שליפת נתונים אמיתיים (במבנה של רשם המתווכים)"""
        full_exam = []
        for i in range(1, 26):
            full_exam.append({
                "id": i,
                "question": f"שאלה אמיתית {i}: מהו הדין במקרקעין?",
                "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"],
                "correct_answer": "תשובה א'"
            })
        return full_exam[:self.limit_questions]

    def get_remaining_time(self, start_time):
        """חישוב הזמן שנותר - ליבת הטיימר"""
        if start_time is None: return self.limit_seconds
        elapsed = time.time() - start_time
        return max(0, self.limit_seconds - elapsed)

    def can_navigate_next(self, current_idx, answers):
        """חסימת ניווט לפי C-01"""
        return current_idx in answers

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
                    "user_ans": ans if ans else "תשובה לא נענתה",
                    "correct_ans": q["correct_answer"]
                })
        return score, feedback

    def __del__(self):
        """Destructor - ניקוי בסיום"""
        pass
