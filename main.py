import streamlit as st
import json
import os

# הגדרות דף נקיות
st.set_page_config(page_title="מערכת בחינה", layout="centered")

def load_exam():
    # טעינת קובץ המקור (העוגן)
    file_path = os.path.join('exams_data', 'test_may_2025_v1.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# אתחול מצב מערכת
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

exam = load_exam()

if exam:
    st.title(exam.get('exam_name', 'בחינה'))
    
    for q in exam['questions']:
        st.write(f"**שאלה {q['question_number']}**")
        st.write(q['question_text'])
        
        # הצגת האפשרויות
        options = q['options']
        user_choice = st.radio(
            "בחר תשובה:",
            options,
            key=f"q_{q['question_number']}",
            index=None,
            disabled=st.session_state.submitted
        )
        
        if user_choice:
            st.session_state.answers[q['question_number']] = user_choice[0]

    st.divider()

    if not st.session_state.submitted:
        if st.button("הגש בחינה"):
            st.session_state.submitted = True
            st.rerun()
    else:
        # חישוב תוצאות
        correct = 0
        for q in exam['questions']:
            u_ans = st.session_state.answers.get(q['question_number'])
            c_ans = q['correct_answer']
            if u_ans == c_ans:
                correct += 1
                st.success(f"שאלה {q['question_number']}: נכון")
            else:
                st.error(f"שאלה {q['question_number']}: טעות (התשובה הנכונה: {c_ans})")
        
        st.balloons()
        st.metric("ציון", f"{(correct/len(exam['questions']))*100:.0f}%")
else:
    st.error("לא נמצא קובץ בחינה תקין בתיקייה.")
