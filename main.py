import streamlit as st
import json
import os

st.set_page_config(page_title="מערכת בחינות")

# CSS לסידור עברית
st.markdown("""<style>.stApp {direction: RTL; text-align: right;}</style>""", unsafe_allow_html=True)

@st.cache_data
def load_exam_data(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # אם ה-JSON עטוף במפתח 'questions', נשלוף רק את הרשימה
                if isinstance(data, dict) and "questions" in data:
                    return data["questions"]
                return data
        except Exception as e:
            return str(e)
    return None

FILE_PATH = "exams_data/test_may1_v1_2025.json"
questions = load_exam_data(FILE_PATH)

if questions is None:
    st.error(f"לא נמצא קובץ בנתיב: {FILE_PATH}")
elif isinstance(questions, str):
    st.error(f"שגיאה בטעינת ה-JSON: {questions}")
elif not isinstance(questions, list):
    st.error("מבנה הקובץ לא תקין. מצפה לרשימה של שאלות.")
else:
    if 'current_idx' not in st.session_state:
        st.session_state.current_idx = 0

    idx = st.session_state.current_idx

    # בדיקת בטיחות לאינדקס
    if idx < len(questions):
        current_q = questions[idx]
        
        st.title(f"שאלה {idx + 1} מתוך {len(questions)}")
        
        # תמיכה בכמה פורמטים של מפתחות
        text = current_q.get('question_text', current_q.get('text', 'שאלה ללא תוכן'))
        st.subheader(text)
        
        options = current_q.get('options', [])
        if options:
            st.radio("בחר תשובה:", options, key=f"q_{idx}")
            if st.button("המשך לשאלה הבאה"):
                st.session_state.current_idx += 1
                st.rerun()
        else:
            st.error("לא נמצאו אפשרויות (options) לשאלה זו.")
    else:
        st.success("הבחינה הסתיימה!")
        if st.button("התחל מחדש"):
            st.session_state.current_idx = 0
            st.rerun()
