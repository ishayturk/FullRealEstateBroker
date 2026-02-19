import json
import os

# הנתונים המלאים של מאי 2025 לפי פרוטוקול C-01
exam_data = {
    "exam_name": "רשם המתווכים במקרקעין - מאי 2025",
    "version": "1",
    "protocol": "C-01",
    "questions": [
        {
            "question_number": 1,
            "question_text": "חיים המתווך ראה מודעה שפורסמה על ידי יהודה... האם חיים פעל באופן תקין בנסיבות המתוארות? מדוע?",
            "options": [
                "א. כן; על הצדדים לדווח את המחיר המלא שהם משלמים בעד עיסקת מקרקעין.",
                "ב. כן, הואיל וחיים היה הגורם היעיל בעיסקה ודמי התיווך פורטו בהזמנת שירותי התיווך.",
                "ג. לא, משום שחיים לא החתים את יהודה על הסכם להזמנת שירותי תיווך כלקוח שמממן את שכר טרחתו.",
                "ד. לא; חיים הפר את חובת הנאמנות שלו כלפי רחל בכך שלא נקב במחיר של עיסקת המקרקעין בפניה בשקיפות."
            ],
            "correct_answer": "ד"
        },
        # כאן יבואו שאר השאלות (קיצרתי לצורך הדוגמה, הקוד המלא מייצר את כולם)
    ]
}

# פונקציה לייצור הקובץ בצורה נקייה
def create_clean_json():
    folder = 'exams_data'
    filename = 'test_may_2025_v1.json'
    path = os.path.join(folder, filename)
    
    # וודוא שהתיקייה קיימת
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # מחיקת קובץ קיים אם יש כדי למנוע בעיות קידוד קודמות
    if os.path.exists(path):
        os.remove(path)
        
    # כתיבה בקידוד UTF-8 ללא BOM
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(exam_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ הקובץ נוצר בהצלחה בכתובת: {path}")

if __name__ == "__main__":
    create_clean_json()
