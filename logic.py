# ==========================================
# Project Identification: C-01
# File: logic.py
# Version: 1218-L4 (Clean Logic)
# Anchor: 1213
# ==========================================
import streamlit as st
import time

def init_exam():
    if 'exam_data' not in st.session_state:
        questions = []
        for i in range(1, 11):
            questions.append({
                "id": i,
                "question": f"שאלה מספר {i}: האם המערכת עובדת?",
                "options": ["כן", "לא", "חלקי", "בבדיקה"],
                "correct": "כן",
                "explanation": f"הסבר לשאלה {i}: בדיקה טכנית של המערכת."
            })
        st.session_state.exam_data = questions
        st.session_state.answers = {}
        st.session_state.current_step = 0 

def run_exam():
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    if remaining <= 0:
        st.error("⚠️ הזמן נגמר!")
        show_finish_button()
        return

    # ניווט צדדי (Sidebar)
    with st.sidebar:
        st.write(f"⏱️ נותר: {remaining} שניות")
        for i in range(10):
            label = f"שאלה {i+1}"
            if i in st.session_state.answers: label = f"✅ {label}"
            if i == st.session_state.current_step: label = f"📍 {label}"
            
            if st.button(label, key=f"side_{i}", use_container_width=True):
                st.session_state.current_step = i
                st.rerun()

    # גוף השאלה
    idx = st.session_state.current_step
    q_item = st.session_state.exam_data[idx]
    
    st.subheader(f"שאלה {idx + 1}")
    st.write(q_item["question"])
    
    ans = st.radio("תשובה:", q_item["options"], key=f"radio_{idx}")
    if ans:
        st.session_state.answers[idx] = ans

    # כפתורי מעבר
    c1, c2 = st.columns(2)
    with c2:
        if idx < 9 and st.button("הבא ⬅️"):
            st.session_state.current_step += 1
            st.rerun()
    with c1:
        if idx > 0 and st.button("➡️ הקודם"):
            st.session_state.current_step -= 1
            st.rerun()

    if len(st.session_state.answers) >= 10:
        show_finish_button()

def show_finish_button():
    if st.button("🏁 סיים בחינה", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    st.header("תוצאות")
    for i, q in enumerate(st.session_state.exam_data):
        st.write(f"שאלה {i+1}: {st.session_state.answers.get(i, 'אין תשובה')}")
