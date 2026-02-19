import streamlit as st
import json
import os

st.set_page_config(page_title="מערכת תרגול למתווכים", layout="wide", initial_sidebar_state="expanded")

def load_exam(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    st.title("🎓 תרגול מבחני רשם המתווכים")
    
    # סריקת קבצי JSON בתיקייה
    exam_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not exam_files:
        st.error("שגיאה: לא נמצאו קבצי JSON בתיקייה.")
        return

    selected_file = st.sidebar.selectbox("בחר מועד:", exam_files)
    
    # אתחול המבחן
    if 'exam_id' not in st.session_state or st.session_state.exam_id != selected_file:
        st.session_state.exam_data = load_exam(selected_file)
        st.session_state.exam_id = selected_file
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    exam = st.session_state.exam_data
    st.header(exam.get('display_title', 'בחינה'))

    # הצגת שאלות
    for q in exam['questions']:
        st.subheader(f"שאלה {q['id']}")
        st.write(q['question'])
        
        q_key = f"q_{q['id']}_{selected_file}" # מפתח ייחודי
        
        if not st.session_state.submitted:
            st.session_state.user_answers[q['id']] = st.radio(
                "בחר תשובה:", q['options'], key=q_key, index=None
            )
        else:
            user_ans = st.session_state.user_answers.get(q['id'])
            correct_ans = q['answer']
            for opt in q['options']:
                if opt == correct_ans:
                    st.success(f"✅ {opt}")
                elif opt == user_ans:
                    st.error(f"❌ {opt} (התשובה שלך)")
                else:
                    st.write(f"⚪ {opt}")
        st.divider()

    # כפתור הגשה וסיכום
    if not st.session_state.submitted:
        if st.button("בדוק תוצאות"):
            st.session_state.submitted = True
            st.rerun()
    else:
        correct_count = sum(1 for q in exam['questions'] if st.session_state.user_answers.get(q['id']) == q['answer'])
        score = (correct_count / len(exam['questions'])) * 100
        st.sidebar.metric("ציון סופי", f"{score:.0f}")
        # השורה שתיקנו:
        st.success(f"המבחן הושלם! ציון: {score:.0f}. תשובות נכונות: {correct_count}/{len(exam['questions'])}")
        
        if st.button("תרגול מחדש"):
            st.session_state.submitted = False
            st.session_state.user_answers = {}
            st.rerun()

if __name__ == "__main__":
    main()
