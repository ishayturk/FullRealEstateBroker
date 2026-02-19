import streamlit as st
import json
import os
import random

# הגדרות דף
st.set_page_config(page_title="מערכת תרגול - רשם המתווכים", layout="wide")

def load_exams():
    exams = []
    data_folder = 'exams_data'
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            if file.endswith('.json'):
                try:
                    with open(os.path.join(data_folder, file), 'r', encoding='utf-8') as f:
                        exams.append(json.load(f))
                except:
                    continue
    return exams

# אתחול Session State
if 'current_exam' not in st.session_state:
    st.session_state.current_exam = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

st.title("📝 תרגול מבחני רשם המתווכים")

exams = load_exams()

if not st.session_state.current_exam:
    st.subheader("בחר מבחן להתחלה:")
    for idx, exam in enumerate(exams):
        if st.button(f"התחל מבחן: {exam['exam_name']}", key=f"btn_{idx}"):
            st.session_state.current_exam = exam
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.rerun()
else:
    exam = st.session_state.current_exam
    st.header(exam['exam_name'])
    
    if st.button("🔙 חזור לבחירת מבחן"):
        st.session_state.current_exam = None
        st.rerun()

    for q in exam['questions']:
        st.write(f"### שאלה {q['question_number']}")
        st.write(q['question_text'])
        
        # בחירת תשובה
        current_ans = st.radio(
            f"בחר תשובה לשאלה {q['question_number']}:",
            q['options'],
            index=None,
            key=f"q_{q['question_number']}",
            disabled=st.session_state.submitted
        )
        
        if current_ans:
            st.session_state.answers[q['question_number']] = current_ans[0] # לוקח רק את האות א', ב' וכו'

    if not st.session_state.submitted:
        if st.button("✅ הגש מבחן"):
            st.session_state.submitted = True
            st.rerun()
    else:
        # הצגת תוצאות
        correct_count = 0
        for q in exam['questions']:
            user_ans = st.session_state.answers.get(q['question_number'])
            correct_ans = q['correct_answer']
            
            if user_ans == correct_ans:
                correct_count += 1
                st.success(f"שאלה {q['question_number']}: נכון! (תשובה {correct_ans})")
            else:
                st.error(f"שאלה {q['question_number']}: טעות. התשובה הנכונה היא {correct_ans}")
        
        score = (correct_count / len(exam['questions'])) * 100
        st.metric("ציון סופי", f"{score:.0f}%", f"{correct_count}/{len(exam['questions'])} תשובות נכונות")
