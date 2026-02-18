# ==========================================
# Project Identification: C-01
# File: logic.py
# Version: 1218-L3 (Sidebar Navigation)
# ==========================================

import streamlit as st
import time

def init_exam():
    if 'exam_data' not in st.session_state:
        questions = []
        for i in range(1, 11):
            questions.append({
                "id": i,
                "question": f"שאלה מספר {i}: האם התפריט הצדדי מופיע?",
                "options": ["כן", "לא", "חלקית", "אולי"],
                "correct": "כן",
                "explanation": f"הסבר לשאלה {i}: זהו הניווט הצדדי המבוקש."
            })
        st.session_state.exam_data = questions
        st.session_state.answers = {}
        st.session_state.current_step = 0 

def run_exam():
    # בדיקת זמן (דקה אחת)
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    if remaining <= 0:
        st.error("⚠️ הזמן נגמר!")
        show_finish_button()
        return

    # --- תפריט צדדי (Sidebar) לניווט ---
    with st.sidebar:
        st.markdown("### 📋 ניווט שאלות")
        st.write(f"⏱️ זמן נותר: {remaining} שניות")
        st.divider()
        
        # יצירת כפתור לכל שאלה
        for i in range(10):
            status = "⚪" # לא נענתה
            if i in st.session_state.answers:
                status = "🔵" # נענתה
            if i == st.session_state.current_step:
                status = "📍" # נוכחית
                
            if st.button(f"{status} שאלה {i+1}", key=f"nav_{i}", use_container_width=True):
                st.session_state.current_step = i
                st.rerun()

    # --- תצוגת השאלה במרכז המסך ---
    idx = st.session_state.current_step
    q_item = st.session_state.exam_data[idx]
    
    st.subheader(f"שאלה {idx + 1} מתוך 10")
    st.write(q_item["question"])
    
    current_answer = st.radio(
        "בחר/י תשובה:", 
        q_item["options"], 
        key=f"q_{idx}",
        index=None if idx not in st.session_state.answers else q_item["options"].index(st.session_state.answers[idx])
    )

    if current_answer:
        st.session_state.answers[idx] = current_answer

    # כפתורי קדימה/אחורה בתחתית
    col1, col2 = st.columns(2)
    with col2:
        if idx < 9 and st.button("לשאלה הבאה ⬅️"):
            st.session_state.current_step += 1
            st.rerun()
    with col1:
        if idx > 0 and st.button("➡️ לשאלה הקודמת"):
            st.session_state.current_step -= 1
            st.rerun()

    if len(st.session_state.answers) >= 10:
        show_finish_button()

def show_finish_button():
    if st.button("🏁 סיים בחינה", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    st.header("📋 תוצאות")
    # ... (אותה לוגיקה של משוב)
    for i, q in enumerate(st.session_state.exam_data):
        with st.expander(f"שאלה {i+1}"):
            st.write(f"תשובה: {st.session_state.answers.get(i)}")
