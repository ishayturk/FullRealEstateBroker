import os
from config import EXAMS_DIR, PROTOCOL, ANCHOR_VERSION

def display_exam_files():
    """
    פונקציית בדיקה: במקום להתחיל בחינה, מציגה את רשימת הקבצים בתיקייה
    """
    print(f"--- דף הסבר לבחינה: בדיקת מאגר (Protocol {PROTOCOL}) ---")
    print(f"עוגן פעיל: {ANCHOR_VERSION}")
    print(f"נתיב תיקייה: {EXAMS_DIR}")
    print("-" * 45)

    try:
        # בדיקה אם התיקייה קיימת
        if not os.path.exists(EXAMS_DIR):
            print(f"❌ שגיאה: התיקייה '{EXAMS_DIR}' לא נמצאה במערכת.")
            return

        # קריאת רשימת הקבצים
        all_files = os.listdir(EXAMS_DIR)
        
        # סינון קבצים לפי הפרוטוקול (test_*.json)
        exam_files = [f for f in all_files if f.startswith('test_') and f.endswith('.json')]

        if not exam_files:
            print("⚠️ התיקייה קיימת, אך אין בה קבצי JSON שעומדים בפרוטוקול.")
        else:
            print(f"✅ נמצאו {len(exam_files)} קבצי בחינה זמינים:")
            for index, file_name in enumerate(sorted(exam_files), 1):
                print(f"  {index}. {file_name}")
            
            print("-" * 45)
            print("בדיקה הושלמה. המערכת מוכנה למעבר לבחינה רנדומלית.")

    except Exception as e:
        print(f"❌ שגיאה במהלך סריקת הקבצים: {e}")

if __name__ == "__main__":
    display_exam_files()
