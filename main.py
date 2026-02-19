import os
import json

EXAMS_DIR = "exams_data"

def check_all_exams():
    print("--- מתחיל סריקת תקינות לקבצי JSON ---")
    
    if not os.path.exists(EXAMS_DIR):
        print(f"❌ שגיאה: התיקייה {EXAMS_DIR} לא קיימת.")
        return

    files = [f for f in os.listdir(EXAMS_DIR) if f.endswith('.json')]
    
    if not files:
        print("⚠️ לא נמצאו קבצי JSON בתיקייה.")
        return

    for file_name in files:
        path = os.path.join(EXAMS_DIR, file_name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"✅ קובץ תקין: {file_name}")
        except json.JSONDecodeError as e:
            print(f"❌ שגיאה נמצאה בקובץ: {file_name}")
            print(f"   פירוט: {e}")
            print(f"   שורה: {e.lineno}, עמודה: {e.colno}")
            print("-" * 30)
        except Exception as e:
            print(f"❌ שגיאה כללית בקובץ {file_name}: {e}")

if __name__ == "__main__":
    check_all_exams()
