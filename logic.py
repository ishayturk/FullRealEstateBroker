# ==========================================
# Project Identification: C-01
# File: logic.py
# Version: 1218-L1 (Core Exam Engine)
# Anchor: 1213
# ==========================================

import streamlit as st
import time
import random

def init_exam():
    """שלב 2+3: בחירת מועד וטעינה לזיכרון (25 שאלות)"""
    if 'exam_data' not in st.session_state:
        # כאן תבוא בעתיד המשיכה מה-URL. כרגע יוצר מבנה דמה ל-25 שאלות.
        questions = []
        for i in range(1, 26):
            questions.append({
                "id": i,
                "question": f"שאלה מספר {i}: מה התשובה הנכונה לדעתך?",
                "options": ["אפשרות א'", "אפשרות ב'", "אפשרות ג'", "אפשרות ד'"],
                "correct": "אפשרות א'",
                "explanation": f"הסבר מלא לשאלה {i}: זו התשובה כי ככה קבענו בעוגן 1213."
            })
        st.session_state.exam_data = questions
        st.session_state.answers = {}
        st.session_state.current_step = 0  # אינדקס השאלה הנוכחית (0-24)

def run_exam():
    """ניהול שלבים 4-7: חוקי התקדמות, ניווט ונעילה"""
    
    # שלב 7: בדיקת זמן (נעילה מוחלטת)
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 180 - int(elapsed))
    
    if remaining <= 0:
        st.error("⚠️ זמן הבחינה הסתיים! המערכת ננעלה למענה וניווט.")
        st.warning("נא ללחוץ על כפתור 'סיים בחינה' בתחתית כדי לראות תוצאות.")
        show_finish_button()
        return # עוצר את הצגת השאלות

    # תצוגת שעון רץ
    st.write(f"⏱️ **זמן נותר: {remaining // 60}:{remaining % 60:02d}**")
    
    # שלב 3: הצגת השאלה הנוכחית (מתוך ה-Chunk של ה-25)
    idx = st.session_state.current_step
    q_item = st.session_state.exam_data[idx]
    
    st.subheader(f"שאלה {idx + 1} מתוך 25")
    st.write(q_item["question"])
    
    # שלב 4: מענה על שאלה
    current_answer = st.radio(
        "בחר/י תשובה:", 
        q_item["options"], 
        key=f"q_{idx}",
        index=None if idx not in st.session_state.answers else q_item["options"].index(st.session_state.answers[idx])
    )

    if current_answer:
        st.session_state.answers[idx] = current_answer

    # שלב 5: ניווט (הבא/קודם)
    col1, col2 = st.columns(2)
    
    with col2: # כפתור הבא - מופיע רק אם ענית
        if current_answer and idx < 24:
            if st.button("שאלה הבאה ⬅️"):
                st.session_state.current_step += 1
                st.rerun()
                
    with col1: # כפתור הקודם - תמיד מאפשר לחזור למה שכבר ענית
        if idx > 0:
            if st.button("➡️ שאלה קודמת"):
                st.session_state.current_step -= 1
                st.rerun()

    # שלב 6: כפתור סיים (מופיע בשאלה 25 או אם ענה על הכל)
    if idx == 24 or len(st.session_state.answers) >= 25:
        show_finish_button()

def show_finish_button():
    st.divider()
    if st.button("🏁 סיים בחינה וקבל משוב", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    """שלב 8: דף משוב וציון"""
    correct_count = 0
    st.header("📋 סיכום תוצאות")
    
    for i, q in enumerate(st.session_state.exam_data):
        user_ans = st.session_state.answers.get(i, "לא נענתה")
        is_correct = user_ans == q["correct"]
        if is_correct: correct_count += 1
        
        with st.expander(f"שאלה {i+1}: {'✅' if is_correct else '❌'}"):
            st.write(f"**השאלה:** {q['question']}")
            st.write(f"**התשובה שלך:** {user_ans}")
            st.write(f"**התשובה הנכונה:** {q['correct']}")
            st.info(f"**הסבר:** {q['explanation']}")
            
    score = int((correct_count / 25) * 100)
    st.success(f"הציון הסופי שלך: {score}")
