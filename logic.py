# ==========================================
# Project Identification: C-01
# File: logic.py
# Version: 1218-L8 (Fix Auto-Skip & Auto-Answer)
# Anchor: 1213
# ==========================================
import streamlit as st
import time

def init_exam():
    # איפוס מוחלט של כל המשתנים כדי למנוע שאריות מהרצה קודמת
    st.session_state.answers = {}
    st.session_state.current_step = 0
    st.session_state.start_time = time.time()
    
    # יצירת השאלות (עוגן 1213)
    questions = []
    for i in range(1, 11):
        questions.append({
            "id": i,
            "question": f"שאלה מספר {i}: האם התשובה נבחרה מראש?",
            "options": ["אופציה א'", "אופציה ב'", "אופציה ג'", "אופציה ד'"],
            "correct": "אופציה א'",
            "explanation": f"הסבר לשאלה {i}"
        })
    st.session_state.exam_data = questions

def run_exam():
    # 1. ניהול זמן
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    if remaining <= 0:
        st.error("⚠️ הזמן נגמר!")
        show_finish_button()
        return

    # 2. Sidebar: ניווט רק למה שנענה או נוכחי
    with st.sidebar:
        st.markdown("### 📋 ניווט")
        st.write(f"⏱️ נותר: {remaining} שניות")
        st.divider()
        
        for idx in range(10):
            if idx in st.session_state.answers or idx == st.session_state.current_step:
                label = f"שאלה {idx + 1}"
                if idx == st.session_state.current_step: label = f"📍 {label}"
                elif idx in st.session_state.answers: label = f"✅ {label}"
                
                if st.button(label, key=f"nav_btn_{idx}", use_container_width=True):
                    st.session_state.current_step = idx
                    st.rerun()

    # 3. תצוגת השאלה
    idx = st.session_state.current_step
    q_item = st.session_state.exam_data[idx]
    
    st.subheader(f"שאלה {idx + 1}")
    st.write(q_item["question"])
    
    # --- התיקון הקריטי: מניעת בחירה מראש ---
    # משתמשים ב-Key שמשתנה בכל פעם שמתחילים מבחן חדש כדי לנקות את ה-Radio
    current_saved = st.session_state.answers.get(idx)
    
    # מציג את האינדקס השמור, או None אם לא נענתה
    if current_saved in q_item["options"]:
        default_idx = q_item["options"].index(current_saved)
    else:
        default_idx = None

    ans = st.radio(
        "בחר/י תשובה:",
        q_item["options"],
        index=default_idx,
        key=f"radio_q_{idx}_session_{st.session_state.start_time}" # Key ייחודי לכל הרצה
    )

    if ans:
        st.session_state.answers[idx] = ans

    # 4. כפתורי שליטה
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if idx > 0:
            if st.button("➡️ הקודם"):
                st.session_state.current_step -= 1
                st.rerun()
    with col2:
        # כפתור הבא מופיע רק אם ענו על השאלה הנוכחית
        if idx < 9 and idx in st.session_state.answers:
            if st.button("שאלה הבאה ⬅️"):
                st.session_state.current_step += 1
                st.rerun()

    if len(st.session_state.answers) >= 10:
        show_finish_button()

def show_finish_button():
    if st.button("🏁 סיים בחינה", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    st.header("📋 תוצאות")
    st.write(f"ענית על {len(st.session_state.answers)} שאלות.")
