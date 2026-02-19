import os
import streamlit as st

# הגדרות פרוטוקול C-01
EXAMS_DIR = "exams_data"
FILE_PREFIX = "test_"
FILE_EXTENSION = ".json"

def get_exam_inventory():
    """סורק את התיקייה ומחזיר רק קבצים שעומדים בפורמט הפרוטוקול"""
    if not os.path.exists(EXAMS_DIR):
        return None, f"התיקייה `{EXAMS_DIR}` לא נמצאה בשרת."
    
    try:
        all_files = os.listdir(EXAMS_DIR)
        # סינון לפי פורמט: מתחיל ב-test_ ומסתיים ב-.json
        filtered_files = [
            f for f in all_files 
            if f.startswith(FILE_PREFIX) and f.endswith(FILE_EXTENSION)
        ]
        return sorted(filtered_files), None
    except Exception as e:
        return None, str(e)

def main():
    st.set_page_config(page_title="בדיקת מאגר בחינות", layout="centered")
    
    st.title("📋 דף הסבר ובדיקת מלאי")
    st.subheader("פרוטוקול C-01 | עוגן 1213")
    
    st.info("המערכת סורקת כעת את תיקיית המבחנים כדי לוודא שכל המועדים מעודכנים.")

    # הרצת הסריקה
    files, error = get_exam_inventory()

    if error:
        st.error(f"❌ שגיאה בסריקה: {error}")
    elif files:
        st.success(f"✅ נמצאו {len(files)} קבצי בחינה תקינים:")
        
        # הצגת הקבצים בפורמט נקי
        for file in files:
            st.code(f"📄 {file}", language="text")
            
        st.divider()
        st.write("💡 **הנחיה:** אם אחד המועדים (מאי, אוגוסט, דצמבר או פברואר) חסר, יש לוודא שהוא הועלה לתיקיית `exams_data` ב-Git.")
    else:
        st.warning("⚠️ התיקייה קיימת אך לא נמצאו קבצים בפורמט `test_*.json`.")

if __name__ == "__main__":
    main()
