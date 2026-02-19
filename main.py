import streamlit as st
import json
import os

# הגדרת עמוד בסיסית (בלי הפרמטר שגרם לשגיאה)
st.set_page_config(page_title="מערכת בחינות")

# הזרקת CSS כדי לתמוך ב-RTL (ימין לשמאל) בלי להפיל את האפליקציה
st.markdown("""
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_exam_data(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

# נתיב הקובץ לפי הפרוטוקול
FILE_PATH = "exams_data/test_may1_v1_2025.json"
questions = load_exam_data(FILE_PATH)

if not questions:
    st.error(f"לא נמצא קובץ נתונים בנתיב: {FILE_PATH}")
    st.info("וודא שהקובץ נמצא בתיקיית exams_data והשם שלו מדויק.")
else:
    if 'current_idx' not in st.session_state:
        st.session_state.current_idx = 0

    idx = st.session_state.current_idx

    if idx < len(questions):
        current_q = questions[idx]
        
        st.title(f"שאלה {idx + 1} מתוך {len(questions)}")
        
        # שימוש ב-get למניעת שגיאות אם מפתח חסר ב-JSON
        q_text = current_q.get('question_text', current_q.get('text', 'טקסט חסר'))
        st.subheader(q_text)
        
        options = current_q.get('options', [])
        if options:
            choice = st.radio("בחר תשובה:", options, key=f"q_{idx}")

            if st.button("המשך לשאלה הבאה"):
                st.session_state.current_idx += 1
                st.rerun()
        else:
            st.warning("לא נמצאו אפשרויות לשאלה זו.")
    else:
        st.success("סיימת את המבחן!")
        if st.button("התחל מחדש"):
            st.session_state.current_idx = 0
            st.rerun()
