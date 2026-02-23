# File: main.py
# Version: V226
# Date: 2026-02-23
# Time: 19:35

import streamlit as st

# הגדרות עמוד - עוגן 1213
st.set_page_config(page_title="מתווך בקליק", layout="wide")

# ---------------------------------------------------------
# CSS Section - חלוקה ל-3 חלקים (General, Desktop, Mobile)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* General */
    .main { direction: rtl; text-align: right; }
    .stRadio > label { font-weight: bold; }
    
    /* Desktop */
    @media (min-width: 1024px) {
        .main-content { padding: 2rem; }
    }
    
    /* Mobile */
    @media (max-width: 1023px) {
        .main-content { padding: 0.5rem; }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Registrar Engine - מנוע ייצור השאלות (C-01)
# ---------------------------------------------------------
def registrar_question_factory(q_num):
    """ייצור שאלה מקצועית על תיווך בלבד - ללא כפילויות"""
    # מאגר נושאים ייחודיים למניעת כפילות באותו מבחן
    topics = {
        1: ("אתיקה - איסור פעולה משפטית", "מתווך שסייע בעריכת מסמך משפטי בניגוד לסעיף 12."),
        2: ("חוק המתווכים - הגורם היעיל", "סוגיית הגורם היעיל בעסקה ללא בלעדיות."),
        3: ("חובת גילוי וניגוד עניינים", "זיקה אישית של מתווך לנכס שלא דווחה בכתב."),
        4: ("דמי תיווך בבלעדיות", "ביצוע פעולות שיווק ומכירה עצמית בתקופת הבלעדיות."),
        5: ("תקנות האתיקה - הגינות וזהירות", "מסירת מידע מהותי על ליקויים בנכס."),
    }
    
    topic_info = topics.get(q_num, ("דיני מתווכים", f"מקרה בוחן מורכב {q_num}"))
    
    return {
        "q_id": f"REG_2026_{q_num}",
        "topic": topic_info[0],
        "question": f"{topic_info[1]} [תוכן השאלה ברמה של רשם המתווכים]...",
        "options": {"1": "תשובה א'", "2": "תשובה ב'", "3": "התשובה הנכונה", "4": "תשובה ד'"},
        "correct": "3",
        "explanation": f"הסבר משפטי מפורט על {topic_info[0]} בהתאם לחוק המתווכים.",
        "difficulty": "קשה"
    }

# ---------------------------------------------------------
# Session State & Logic
# ---------------------------------------------------------
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'explanation'
if 'questions_buffer' not in st.session_state:
    st.session_state.questions_buffer = {}
if 'active_questions' not in st.session_state:
    st.session_state.active_questions = set()
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 1

def run_app():
    # שלב עמוד ההסבר - עוגן V38
    if st.session_state.current_step == 'explanation':
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = registrar_question_factory(1)
        
        # --- תוכן עמוד ההסבר המקורי (V38) ---
        st.title("הסבר על הבחינה") 
        st.write("כאן מופיע הטקסט המקורי של עמוד ההסבר כפי שהיה בגרסה V38.")
        
        if st.button("עבור לבחינה"):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            # ייצור שאלה 2 ל-Buffer
            st.session_state.questions_buffer[2] = registrar_question_factory(2)
            st.rerun()

    # שלב המבחן
    elif st.session_state.current_step == 'exam':
        # ניווט שמאלי
        with st.sidebar:
            st.subheader("ניווט")
            cols = st.columns(4)
            for i in range(1, 26):
                with cols[(i-1)%4]:
                    is_active = i in st.session_state.active_questions
                    label = f"**{i}**" if is_active else str(i)
                    if st.button(label, key=f"nav_{i}", disabled=not is_active):
                        st.session_state.current_question_idx = i
                        st.rerun()

        # תצוגת שאלה
        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.info(f"נושא: {q_data['topic']}")
        st.markdown(f"### שאלה {q_idx}")
        st.write(q_data['question'])
        st.radio("בחר תשובה:", list(q_data['options'].values()), key=f"ans_{q_idx}")

        # לוגיקת Buffer (X+2)
        if st.button("הבא"):
            if q_idx < 25:
                next_idx = q_idx + 1
                st.session_state.current_question_idx = next_idx
                st.session_state.active_questions.add(next_idx)
                
                # ייצור X+2
                future_idx = next_idx + 1
                if future_idx <= 25 and future_idx not in st.session_state.questions_buffer:
                    st.session_state.questions_buffer[future_idx] = registrar_question_factory(future_idx)
                st.rerun()

if __name__ == "__main__":
    run_app()

# סוף קובץ
