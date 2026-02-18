# ==========================================
# Project Identification: C-01
# File: logic.py
# Version: 1218-L7 (Progressive Navigation)
# ==========================================
import streamlit as st
import time

def init_exam():
    if 'exam_data' not in st.session_state:
        # יצירת 10 שאלות (עוגן 1213)
        questions = []
        for i in range(1, 11):
            questions.append({
                "id": i,
                "question": f"שאלה מספר {i}: האם ניתן לנווט קדימה?",
                "options": ["כן", "לא", "רק מה שעניתי", "אולי"],
                "correct": "רק מה שעניתי",
                "explanation": "ניווט מתאפשר רק לשאלות קודמות שנענו."
            })
        st.session_state.exam_data = questions
        st.session_state.answers = {}
        st.session_state.current_step = 0 

def run_exam():
    # 1. ניהול זמן
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    if remaining <= 0:
        st.error("⚠️ הזמן נגמר!")
        show_finish_button()
        return

    # 2. Sidebar: מציג רק את מה שרלוונטי לניווט כרגע
    with st.sidebar:
        st.markdown("### 📋 ניווט שאלות")
        st.write(f"⏱️ נותר: {remaining} שניות")
        st.divider()
        
        # לולאה על כל 10 השאלות
        for idx in range(10):
            # תנאי: הכפתור יופיע רק אם השאלה נענתה OR זו השאלה הנוכחית
            if idx in st.session_state.answers or idx == st.session_state.current_step:
                label = f"שאלה {idx + 1}"
                if idx == st.session_state.current_step:
                    label = f"📍 {label}"
                elif idx in st.session_state.answers:
                    label = f"✅ {label}"
                
                if st.button(label, key=f"nav_{idx}", use_container_width=True):
                    st.session_state.current_step = idx
                    st.rerun()
            # שאלות עתידיות פשוט לא מופיעות ב-Sidebar

    # 3. תצוגת השאלה
    idx = st.session_state.current_step
    q_item = st.session_state.exam_data[idx]
    
    st.divider()
    st.subheader(f"שאלה {idx + 1} מתוך 10")
    st.write(q_item["question"])
    
    # ניהול תשובה שנבחרה (ברירת מחדל ריקה)
    current_saved = st.session_state.answers.get(idx)
    default_idx = q_item["options"].index(current_saved) if current_saved in q_item["options"] else None

    ans = st.radio("בחר/י תשובה:", q_item["options"], index=default_idx, key=f"r_{idx}")

    # שמירת התשובה במידה ונבחרה
    if ans:
        st.session_state.answers[idx] = ans

    # 4. כפתורי שליטה בתחתית
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if idx > 0:
            if st.button("➡️ הקודם"):
                st.session_state.current_step -= 1
                st.rerun()
    with col2:
        # כפתור "הבא" יופיע רק אם ענו על השאלה הנוכחית
        if idx < 9 and idx in st.session_state.answers:
            if st.button("שאלה הבאה ⬅️"):
                st.session_state.current_step += 1
                st.rerun()

    # כפתור סיום מופיע רק בסוף
    if len(st.session_state.answers) >= 10:
        st.divider()
        show_finish_button()

def show_finish_button():
    if st.button("🏁 סיים בחינה", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    st.header("📋 תוצאות")
    st.write(f"ענית על {len(st.session_state.answers)} שאלות.")
