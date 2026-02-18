# ==========================================
# Project Identification: C-01
# File: logic.py
# Version: 1218-L2 (Quick Simulation: 10Q, 1M)
# ==========================================

import streamlit as st
import time

def init_exam():
    """שלב 2+3: טעינת 10 שאלות לזיכרון"""
    if 'exam_data' not in st.session_state:
        questions = []
        for i in range(1, 11): # מקוצר ל-10 שאלות
            questions.append({
                "id": i,
                "question": f"שאלה מספר {i}: האם המערכת מיושרת לימין?",
                "options": ["כן, הכל בסדר", "לא, עדיין יש בעיה", "חלקית", "לא יודע"],
                "correct": "כן, הכל בסדר",
                "explanation": f"הסבר לשאלה {i}: בעוגן 1213 הגדרנו יישור לימין (RTL) כחובה."
            })
        st.session_state.exam_data = questions
        st.session_state.answers = {}
        st.session_state.current_step = 0 

def run_exam():
    """ניהול שלבים 4-7: טיימר לדקה אחת וניווט סליידר"""
    
    # שלב 7: בדיקת זמן (60 שניות)
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed)) # שונה לדקה אחת
    
    if remaining <= 0:
        st.error("⚠️ הזמן נגמר! נא ללחוץ על 'סיים בחינה' למטה.")
        show_finish_button()
        return

    # תצוגת שעון
    st.metric("זמן נותר (שניות)", remaining)
    
    # שלב 5: סליידר ניווט (מופיע רק לשאלות שנענו)
    answered_indices = sorted(list(st.session_state.answers.keys()))
    if answered_indices:
        st.write("---")
        st.write("**ניווט מהיר לשאלות שנענו:**")
        nav_idx = st.select_slider(
            "בחר שאלה:",
            options=range(1, 11),
            value=st.session_state.current_step + 1
        )
        if nav_idx - 1 != st.session_state.current_step:
            st.session_state.current_step = nav_idx - 1
            st.rerun()

    # הצגת השאלה
    idx = st.session_state.current_step
    q_item = st.session_state.exam_data[idx]
    
    st.subheader(f"שאלה {idx + 1} מתוך 10")
    st.write(q_item["question"])
    
    # שלב 4: מענה
    current_answer = st.radio(
        "בחר/י תשובה:", 
        q_item["options"], 
        key=f"q_{idx}",
        index=None if idx not in st.session_state.answers else q_item["options"].index(st.session_state.answers[idx])
    )

    if current_answer:
        st.session_state.answers[idx] = current_answer

    # כפתורי ניווט
    col1, col2 = st.columns(2)
    with col2:
        if current_answer and idx < 9: # עד שאלה 10
            if st.button("שאלה הבאה ⬅️"):
                st.session_state.current_step += 1
                st.rerun()
    with col1:
        if idx > 0:
            if st.button("➡️ שאלה קודמת"):
                st.session_state.current_step -= 1
                st.rerun()

    if idx == 9 or len(st.session_state.answers) >= 10:
        show_finish_button()

def show_finish_button():
    st.divider()
    if st.button("🏁 סיים בחינה", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    """שלב 8: דף משוב (RTL מלא)"""
    st.header("📋 תוצאות הבחינה")
    correct_count = 0
    
    for i, q in enumerate(st.session_state.exam_data):
        user_ans = st.session_state.answers.get(i, "לא נענתה")
        is_correct = user_ans == q["correct"]
        if is_correct: correct_count += 1
        
        with st.expander(f"שאלה {i+1}: {'✅' if is_correct else '❌'}"):
            st.write(f"**התשובה שלך:** {user_ans}")
            st.write(f"**התשובה הנכונה:** {q['correct']}")
            st.info(f"**הסבר:** {q['explanation']}")
            
    st.success(f"ציון סופי: {int((correct_count/10)*100)}")
