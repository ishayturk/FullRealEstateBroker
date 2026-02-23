# File: logic.py
# Version: V220
# Date: 2026-02-23
# Time: 17:45

import streamlit as st
import json
import os

def load_exam_data(exam_name):
    """טעינת נתוני מבחן מתיקיית exams_data"""
    file_path = f"exams_data/{exam_name}.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def generate_question_logic(exam_data, question_num):
    """לוגיקת שליפת שאלה מהמאגר (הדמיית ייצור ב-Buffer)"""
    if not exam_data or str(question_num) not in exam_data['questions']:
        return None
    
    q_data = exam_data['questions'][str(question_num)]
    return {
        "number": question_num,
        "text": q_data['text'],
        "options": q_data['options'],
        "correct_answer": q_data['correct_index']
    }

def init_session_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'explanation'
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 1
    if 'questions_buffer' not in st.session_state:
        st.session_state.questions_buffer = {}
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'active_questions' not in st.session_state:
        st.session_state.active_questions = set()
    if 'exam_finished' not in st.session_state:
        st.session_state.exam_finished = False

def render_exam_page():
    init_session_state()
    
    # שלב ההתנעה: עמוד הסבר מייצר את שאלה 1
    if st.session_state.current_step == 'explanation':
        if 1 not in st.session_state.questions_buffer:
            exam_data = load_exam_data("test_may1_v1_2025")
            st.session_state.questions_buffer[1] = generate_question_logic(exam_data, 1)
        
        # הצגת עמוד ההסבר הקיים (ללא שינויי עיצוב)
        st.title("מבחן רישויי למתווכים - הסברים")
        if st.button("התחל בחינה"):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            # לחיצה על התחל מייצרת את שאלה 2 ברקע
            exam_data = load_exam_data("test_may1_v1_2025")
            st.session_state.questions_buffer[2] = generate_question_logic(exam_data, 2)
            st.rerun()

    # מהלך הבחינה
    elif st.session_state.current_step == 'exam':
        q_idx = st.session_state.current_question_idx
        
        # לוגיקת ניווט אקטיבי: שאלה הופכת ל-Bold ברגע שנטענה
        st.session_state.active_questions.add(q_idx)
        
        question = st.session_state.questions_buffer.get(q_idx)
        
        st.markdown(f"## שאלה {q_idx}")
        st.write(question['text'])
        
        # תשובות
        options = question['options']
        user_choice = st.radio("בחר תשובה:", options, index=None, key=f"q_{q_idx}")
        
        if user_choice:
            st.session_state.user_answers[q_idx] = options.index(user_choice)

        # כפתורי ניווט
        col_prev, col_finish, col_next = st.columns(3)
        
        with col_prev:
            if q_idx > 1:
                if st.button("לשאלה הקודמת"):
                    st.session_state.current_question_idx -= 1
                    st.rerun()
        
        with col_finish:
            # כפתור סיים בחינה מופיע משאלה 25 ונשאר קבוע
            if q_idx == 25 and q_idx in st.session_state.user_answers:
                st.session_state.exam_finished = True
            
            if st.session_state.exam_finished:
                if st.button("סיים בחינה"):
                    st.session_state.current_step = 'feedback'
                    st.rerun()

        with col_next:
            if q_idx < 25:
                # כפתור הבא לחיץ רק אם סומנה תשובה
                is_disabled = q_idx not in st.session_state.user_answers
                if st.button("לשאלה הבאה", disabled=is_disabled):
                    next_q = q_idx + 1
                    st.session_state.current_question_idx = next_q
                    
                    # לוגיקת Buffer: בשאלה X לחיצה מייצרת את X+2 (עד שאלה 23 שמייצרת את 25)
                    if next_q < 25:
                        future_q = next_q + 1
                        if future_q not in st.session_state.questions_buffer:
                            exam_data = load_exam_data("test_may1_v1_2025")
                            st.session_state.questions_buffer[future_q] = generate_question_logic(exam_data, future_q)
                    st.rerun()

    elif st.session_state.current_step == 'feedback':
        st.write("דף משוב")

# סוף קובץ
