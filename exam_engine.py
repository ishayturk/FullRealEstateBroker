import requests
from bs4 import BeautifulSoup
import time
import random

class ExamSystem:
    def __init__(self, user_name="חיים חיים"):
        self.user_name = user_name
        self.anchor_file = "1213.txt"  # עוגן הלמידה
        self.base_url = "https://www.reba.org.il/files/%D7%91%D7%97%D7%99%D7%A0%D7%95%D7%AA--%D7%9C%D7%93%D7%95%D7%92%D7%9E%D7%90--%D7%9C%D7%A7%D7%91%D7%9C%D7%AA--%D7%A8%D7%99%D7%A9%D7%99%D7%95%D7%9F--%D7%AA%D7%99%D7%95%D7%95%D7%9A/"
        
        # פרמטרים לבדיקה הנוכחית
        self.test_limit_questions = 10
        self.test_limit_minutes = 2
        
        self.current_exam_questions = []
        self.user_answers = {}

    def fetch_exam_data(self):
        """
        שליפת בחינה שלמה מהמקור הרשמי.
        בשלב זה הפונקציה מדמה שליפה מה-URL ופירוק ה-HTML לשאלות אמיתיות.
        """
        try:
            # כאן תבוצע השליפה האמיתית מהאתר
            # response = requests.get(self.base_url)
            # soup = BeautifulSoup(response.content, 'html.parser')
            
            # לוגיקת פירוק זמנית המייצגת מבנה אמיתי (עד לחיבור הסופי של ה-Scraper)
            all_questions = self._parse_mock_real_data() 
            
            # בחירת בחינה שלמה (כאן אנחנו לוקחים את 10 הראשונות לצורך הבדיקה)
            self.current_exam_questions = all_questions[:self.test_limit_questions]
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False

    def _parse_mock_real_data(self):
        """
        מדמה את המבנה שיוצא מה-Parser של אתר רשם המתווכים.
        """
        mock_data = []
        for i in range(1, 26): # בחינה שלמה של 25 שאלות
            mock_data.append({
                "id": i,
                "question": f"שאלה אמיתית מהאתר מספר {i}: מה הדין במקרה של...",
                "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"],
                "correct_index": 0 # יימשך מעמודת התשובות במועד הרלוונטי
            })
        return mock_data

    def start_exam(self):
        print(f"שלום {self.user_name}, המבחן מתחיל.")
        print(f"מוקצבות לך {self.test_limit_minutes} דקות ל-{self.test_limit_questions} שאלות.")
        print("-" * 30)
        
        start_time = time.time()
        end_time = start_time + (self.test_limit_minutes * 60)

        for i, q in enumerate(self.current_exam_questions):
            # בדיקת זמן
            if time.time() > end_time:
                print("\n!!! הזמן הסתיים !!!")
                break

            print(f"\nשאלה {i+1}: {q['question']}")
            for idx, opt in enumerate(q['options']):
                print(f"{idx+1}. {opt}")

            # חסימת ניווט - חייב לענות
            choice = None
            while choice is None:
                try:
                    user_input = input("בחר תשובה (1-4): ")
                    val = int(user_input) - 1
                    if 0 <= val <= 3:
                        choice = val
                    else:
                        print("בחר מספר בין 1 ל-4.")
                except ValueError:
                    print("קלט לא תקין.")

            self.user_answers[i] = choice

        self.show_feedback()

    def show_feedback(self):
        print("\n" + "="*20)
        print("תוצאות הבחינה:")
        correct_count = 0
        
        for i, q in enumerate(self.current_exam_questions):
            user_idx = self.user_answers.get(i)
            is_correct = user_idx == q['correct_index']
            
            if is_correct:
                correct_count += 1
                print(f"שאלה {i+1}: V")
            else:
                user_text = q['options'][user_idx] if user_idx is not None else "תשובה לא נענתה"
                correct_text = q['options'][q['correct_index']]
                print(f"שאלה {i+1}: X")
                print(f"התשובה שלך: {user_text}")
                print(f"\nהתשובה הנכונה: {correct_text}")
                print("-" * 10)

        print(f"\nציון סופי: {correct_count} מתוך {len(self.current_exam_questions)}")

# הרצה לבדיקה
if __name__ == "__main__":
    exam = ExamSystem()
    if exam.fetch_exam_data():
        exam.start_exam()
