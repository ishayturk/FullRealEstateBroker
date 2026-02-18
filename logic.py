import time

# גרסה: D-3000 | מזהה קובץ: C-01
class ExamManager:
    def __init__(self, user_name="חיים חיים"):
        self.user_name = user_name
        self.limit_questions = 10
        self.limit_seconds = 120
        self.questions = self._get_real_broker_questions()

    def _get_real_broker_questions(self):
        """שאלות אמיתיות מעוגן 1213"""
        return [
            {"question": "מהו התנאי לקבלת רישיון תיווך לפי חוק המתווכים?", "options": ["אזרח ישראל", "מלאו לו 18 שנים", "לא הוכרז כפושט רגל", "כל התשובות נכונות"], "correct": "כל התשובות נכונות"},
            {"question": "האם מתווך רשאי לסייע בעריכת מסמך בעל אופי משפטי?", "options": ["כן, אם זה זיכרון דברים", "רק אם הוא מוסמך כעורך דין", "לא, חל איסור מוחלט בחוק", "כן, במידה והלקוח ביקש"], "correct": "לא, חל איסור מוחלט בחוק"},
            {"question": "מהי תקופת הבלעדיות המקסימלית בדירת מגורים?", "options": ["3 חודשים", "6 חודשים", "9 חודשים", "שנה"], "correct": "6 חודשים"},
            {"question": "מתווך שפעל ללא רישיון בתוקף:", "options": ["זכאי לחצי דמי תיווך", "זכאי לדמי תיווך רק מהמוכר", "אינו זכאי לדמי תיווך כלל", "יקבל דמי תיווך כהחזר הוצאות"], "correct": "אינו זכאי לדמי תיווך כלל"},
            {"question": "הזמנה בכתב לביצוע פעולת תיווך חייבת לכלול:", "options": ["שמות וכתובות הצדדים", "סוג העסקה", "מחיר העסקה בקירוב", "כל התשובות נכונות"], "correct": "כל התשובות נכונות"},
            {"question": "חובת ההגינות והזהירות של מתווך היא כלפי:", "options": ["הלקוח שלו בלבד", "כלפי שני הצדדים לעסקה", "כלפי הרשם בלבד", "רק כלפי מי שמשלם"], "correct": "כלפי שני הצדדים לעסקה"},
            {"question": "מי רשאי לעסוק בתיווך מקרקעין?", "options": ["כל מי שפתח עוסק מורשה", "רק מי שבידו רישיון תקף", "מי שעבר התמחות של שנה", "חברות בע\"מ בלבד"], "correct": "רק מי שבידו רישיון תקף"},
            {"question": "על פי החוק, מתווך בבלעדיות חייב לבצע:", "options": ["לפחות 2 פעולות שיווק", "פרסום בעיתון יומי בלבד", "שלט על הנכס בלבד", "אין חובת שיווק בחוק"], "correct": "לפחות 2 פעולות שיווק"},
            {"question": "דמי תיווך ישולמו למתווך כאשר:", "options": ["הוא היה הגורם היעיל בעסקה", "הוא פרסם את הנכס ראשון", "הלקוח חתם על טופס בלבד", "העסקה התפוצצה בגלל המוכר"], "correct": "הוא היה הגורם היעיל בעסקה"},
            {"question": "תקופת הבלעדיות בנכס שאינו דירת מגורים:", "options": ["מוגבלת לחצי שנה", "אינה מוגבלת בזמן", "מוגבלת לשנה אחת", "מוגבלת ל-3 חודשים"], "correct": "אינה מוגבלת בזמן"}
        ]

    def get_remaining_time(self, start_time):
        if start_time is None: return self.limit_seconds
        elapsed = time.time() - start_time
        return max(0, self.limit_seconds - elapsed)

    def process_results(self, user_answers):
        score = 0
        feedback = []
        for i, q in enumerate(self.questions):
            ans = user_answers.get(i)
            is_correct = (ans == q["correct"])
            if is_correct:
                score += 1
                feedback.append({"id": i+1, "status": "V"})
            else:
                feedback.append({"id": i+1, "status": "X", "user_ans": ans if ans else "לא ענית", "correct_ans": q["correct"]})
        return score, feedback
