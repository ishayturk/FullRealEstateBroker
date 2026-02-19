import json

# מזהה קבצים: C-01
# גרסה: 1218-G2-FINAL-TIMER-FIX
# לוגיקת מבחן רישוי למתווכים - כולל טיימר רציף ומשוב מפורט

class ExamLogic:
    def __init__(self, exam_data, total_time_minutes=120):
        self.questions = exam_data['questions']
        self.total_questions = len(self.questions)
        self.user_answers = {}  # {שאלה_אינדקס: "אות_תשובה"}
        self.current_index = 0
        self.time_left_seconds = total_time_minutes * 60
        self.timeout_occurred = False
        self.is_last_answered = False

    def get_current_question(self):
        """מחזיר את השאלה הנוכחית להצגה"""
        return self.questions[self.current_index]

    def select_answer(self, answer_letter):
        """שמירת תשובה ועדכון דגל שאלה 25"""
        if not self.timeout_occurred:
            self.user_answers[self.current_index] = answer_letter
            if self.current_index == 24: # שאלה 25 נענתה
                self.is_last_answered = True

    def update_timer(self):
        """עדכון הטיימר בכל שנייה - נקרא מה-Frontend"""
        if self.time_left_seconds > 0:
            self.time_left_seconds -= 1
        else:
            self.timeout_occurred = True
        return self.time_left_seconds

    def navigate(self, direction):
        """ניווט: 'next' רק אם ענה, 'prev' תמיד (עד שאלה 1)"""
        if self.timeout_occurred:
            return # חסימת ניווט בזמן Timeout

        if direction == "next" and self.current_index < self.total_questions - 1:
            if self.current_index in self.user_answers:
                self.current_index += 1
        elif direction == "prev" and self.current_index > 0:
            self.current_index -= 1

    def calculate_results(self):
        """חישוב ציון ויצירת דף משוב מפורט לפי הפרוטוקול"""
        correct_count = 0
        summary = []
        
        for i, q in enumerate(self.questions):
            user_ans = self.user_answers.get(i)
            correct_ans = q['correct_answer']
            is_correct = (user_ans == correct_ans)
            
            if is_correct:
                correct_count += 1
                detail = f"ענית {user_ans}. (נכון)"
            elif user_ans is None:
                # לוגיקה לשאלה שלא נענתה (זמן נגמר)
                detail = f"תשובה לא נענתה. התשובה הנכונה: {correct_ans} - {q['options'][correct_ans]}"
            else:
                # תשובה שגויה - הצגת מלל מלא להשוואה
                detail = f"ענית: {user_ans} - {q['options'][user_ans]}. " \
                         f"התשובה הנכונה: {correct_ans} - {q['options'][correct_ans]}"
            
            summary.append({
                "num": i + 1,
                "status": "✅" if is_correct else "❌",
                "detail": detail
            })
            
        score = round((correct_count / self.total_questions) * 100)
        return score, summary

    def get_ui_state(self):
        """מחזיר את מצב הממשק המלא לרינדור"""
        return {
            "question": self.get_current_question(),
            "current_num": self.current_index + 1,
            "can_go_next": (self.current_index in self.user_answers) and (self.current_index < 24),
            "can_go_prev": self.current_index > 0,
            "show_finish": self.is_last_answered or self.timeout_occurred,
            "is_locked": self.timeout_occurred,
            "sidebar": self._generate_sidebar()
        }

    def _generate_sidebar(self):
        """סייד-
