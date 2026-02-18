import time

# גרסת קובץ: D-3000
# עוגן לוגי: C-01
TEST_LIMIT_QUESTIONS = 10
TEST_LIMIT_SECONDS = 120 

def get_real_exam_data():
    """שליפת נתוני בחינה - גרסה D-3000"""
    full_exam = []
    # מדמה מבנה בחינה אמיתית שתגיע מה-Scraper
    for i in range(1, 26):
        full_exam.append({
            "id": i,
            "question": f"שאלה אמיתית {i} מהאתר: מהו הדין במקרה של...",
            "options": ["תשובה א'", "תשובה ב'", "תשובה ג'", "תשובה ד'"],
            "correct_answer": "תשובה א'"
        })
    return full_exam[:TEST_LIMIT_QUESTIONS]

def manage_exam_timer(start_time):
    if start_time is None:
        return TEST_LIMIT_SECONDS
    elapsed = time.time() - start_time
    remaining = max(0, TEST_LIMIT_SECONDS - elapsed)
    return remaining

def can_move_next(current_q_idx, answers_dict):
    return current_q_idx in answers_dict

def process_results(questions, user_answers):
    score = 0
    feedback_data = []
    for i, q in enumerate(questions):
        user_choice = user_answers.get(i)
        correct_choice = q["correct_answer"]
        is_correct = (user_choice == correct_choice)
        if is_correct:
            score += 1
            feedback_data.append({"id": i + 1, "status": "V"})
        else:
            feedback_data.append({
                "id": i + 1,
                "status": "X",
                "user_ans": user_choice if user_choice else "תשובה לא נענתה",
                "correct_ans": correct_choice
            })
    return score, feedback_data
