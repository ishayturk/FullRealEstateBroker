import os
import json
import streamlit as st

EXAMS_DIR = "exams_data"

def main():
    st.title("🔍 סורק תקינות קבצי JSON")
    st.write("בודק את כל הקבצים בתיקיית `exams_data`...")

    if not os.path.exists(EXAMS_DIR):
        st.error(f"התיקייה `{EXAMS_DIR}` לא נמצאה.")
        return

    files = [f for f in os.listdir(EXAMS_DIR) if f.endswith('.json')]
    
    if not files:
        st.warning("לא נמצאו קבצי JSON.")
        return

    for file_name in files:
        path = os.path.join(EXAMS_DIR, file_name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                json.load(f)
            st.success(f"✅ קובץ תקין: {file_name}")
        except json.JSONDecodeError as e:
            st.error(f"❌ שגיאה בקובץ: **{file_name}**")
            st.warning(f"פירוט: {e}")
            st.info(f"שורה: {e.lineno}, עמודה: {e.colno}")
            st.divider()
        except Exception as e:
            st.error(f"שגיאה כללית ב-{file_name}: {e}")

if __name__ == "__main__":
    main()
