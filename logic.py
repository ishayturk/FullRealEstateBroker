import streamlit as st
import time

def init_exam():
    st.session_state.answers = {}
    st.session_state.current_step = 0
    st.session_state.start_time = time.time()
    
    # טעינת 10 שאלות (עוגן 1213)
    questions = []
    for i in range(1, 11):
        questions.append({
            "id": i,
            "question": f"שאלה {i} מתוך 10",
            "options": ["תשובה 1", "תשובה 2", "תשובה 3", "תשובה 4"],
            "correct": "תשובה 1"
        })
    st.session_state.exam_data = questions

def run_exam():
    # חישוב זמן
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 60 - int(elapsed))
    
    # טיימר רץ בראש הדף
    st.markdown(f"### ⏱️ זמן נותר: {remaining} שניות")
    
    if remaining <= 0:
        st.error("הזמן נגמר")
        show_finish_button()
        return

    # סיידבר - ניווט מותנה (רק מה שנענה או נוכחי)
    with st.sidebar:
        st.write("ניווט")
        for i in range(10):
            if i in st.session_state.answers or i == st.session_state.current_step:
                lbl = f"שאלה {i+1}"
                if i == st.session_state.current_step: lbl = f"📍 {lbl}"
                elif i in st.session_state.answers: lbl = f"✅ {lbl}"
                
                if st.button(lbl, key=f"n_{i}", use_container_width=True):
                    st.session_state.current_step = i
                    st.rerun()

    # תצוגה בימין (באמצעות עמודות)
    idx = st.session_state.current_step
    q = st.session_state.exam_data[idx]
    
    _, col = st.columns([1, 10])
    with col:
        st.subheader(f"שאלה {idx + 1}")
        st.write(q["question"])
        
        # בחירה ריקה (None) ושימוש ב-Key ייחודי לאיפוס
        ans_key = f"q_{idx}_{st.session_state.start_time}"
        current = st.session_state.answers.get(idx)
        def_idx = q["options"].index(current) if current in q["options"] else None

        ans = st.radio("בחר תשובה:", q["options"], index=def_idx, key=ans_key)
        if ans:
            st.session_state.answers[idx] = ans

        # ניווט תחתון
        st.write("")
        b1, b2 = st.columns(2)
        with b1:
            if idx > 0:
                if st.button("➡️ הקודם"):
                    st.session_state.current_step -= 1
                    st.rerun()
        with b2:
            if idx < 9 and idx in st.session_state.answers:
                if st.button("הבא ⬅️"):
                    st.session_state.current_step += 1
                    st.rerun()

    # סיום
    if len(st.session_state.answers) >= 10:
        st.divider()
        show_finish_button()

    # רענון טיימר
    time.sleep(1)
    st.rerun()

def show_finish_button():
    if st.button("🏁 סיים בחינה", type="primary", use_container_width=True):
        st.session_state.page_state = 'results'
        st.rerun()

def calculate_results():
    st.header("תוצאות")
    st.write(f"ענית על {len(st.session_state.answers)} שאלות.")
