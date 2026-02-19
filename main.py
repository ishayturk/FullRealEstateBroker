import os
import json
import streamlit as st

# הגדרות פרוטוקול C-01
EXAMS_DIR = "exams_data"
FILE_PREFIX = "test_"
FILE_EXTENSION = ".json"

def read_first_questions(file_path):
    """קריאת שתי השאלות הראשונות מקובץ JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # הנחה שהשאלות נמצאות תחת מפתח בשם 'questions' לפי פרוטוקול C-01
            questions = data.get('questions', [])
            return questions[:2], None
    except Exception as e:
        return None, str(e)

def main():
    st.set_page_config(page_title="מערכת בחינות - בדיקה", layout="centered")
    
    st.title("📖 דף הסבר למבחן")
    
    st.write("""
    ברוכים הבאים למבחן המתווך. 
    לפני שתתחילו, אנא קראו את ההוראות:
    * יש לענות על כל השאלות לפי הסדר.
    * אין אפשרות לחזור אחורה לאחר מעבר שאלה.
    * המבחן מוגבל בזמן.
    """)

    # שלב האישור
    confirmed = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל")
    
    if st.button("מעבר לבחינה"):
        if not confirmed:
            st.warning("יש לסמן את התיקייה שקראת את ההוראות לפני המעבר.")
        else:
            st.divider()
            st.subheader("🔍 הרצת בדיקת סנכרון (דיאגנוסטיקה)")

            # 1. סריקת התיקייה
            if not os.path.exists(EXAMS_DIR):
                st.error(f"❌ תקלה: התיקייה `{EXAMS_DIR}` חסרה.")
                return

            all_files = os.listdir(EXAMS_DIR)
            exam_files = sorted([f for f in all_files if f.startswith(FILE_PREFIX) and f.endswith(FILE_EXTENSION)])

            if not exam_files:
                st.error("❌ לא נמצאו קבצי בחינה תקינים.")
            else:
                st.success(f"✅ נמצאו {len(exam_files)} קבצים. בודק תוכן של הקובץ הראשון...")
                
                # 2. בדיקת קריאה מהקובץ הראשון ברשימה
                target_file = os.path.join(EXAMS_DIR, exam_files[0])
                questions, err = read_first_questions(target_file)

                if err:
                    st.error(f"❌ שגיאה בקריאת הקובץ `{exam_files[0]}`: {err}")
                elif questions:
                    st.write(f"📂 **נבדק קובץ:** `{exam_files[0]}`")
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**שאלה {i}:**")
                        # שליפת השאלה (תלוי במבנה ה-JSON הספציפי שלך)
                        question_text = q.get('question_text') or q.get('text') or str(q)
                        st.info(question_text)
                    
                    st.success("🏁 בדיקת ה-JSON עברה בהצלחה. הקוד מוכן להרצה.")
                else:
                    st.warning("הקובץ נמצא אך נראה שהוא ריק משאלות.")

if __name__ == "__main__":
    main()
