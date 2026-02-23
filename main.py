# File: main.py
# Version: V224
# Date: 2026-02-23
# Time: 18:45

import streamlit as st

# הגדרות עמוד
st.set_page_config(page_title="מערכת רשם המתווכים", layout="wide")

# ---------------------------------------------------------
# CSS Section - מופרד ל-3 חלקים כפי שהוגדר בפרוטוקול
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. General Section */
    .main { direction: rtl; text-align: right; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; }
    .stRadio > label { font-size: 1.1rem; font-weight: bold; }
    
    /* 2. Desktop Section */
    @media (min-width: 1024px) {
        .stSidebar { width: 300px !important; }
        .main-content { padding: 3rem; }
    }
    
    /* 3. Mobile Section */
    @media (max-width: 1023px) {
        .stSidebar { width: 100% !important; }
        .main-content { padding: 0.5rem; }
        h1 { font-size: 1.4rem; }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Registrar Engine - מנוע ייצור השאלות (C-01)
# ---------------------------------------------------------
def registrar_question_factory(q_num):
    """מייצר שאלה ייחודית ומורכבת 'על הדרך' ללא כפילויות"""
    
    # מאגר נושאים ייחודיים (למידה מבחינות מאי 25, אוגוסט 24, פברואר 25)
    topics_map = {
        1: ("אתיקה - איסור פעולה משפטית", "מתווך שסייע בניסוח הסכם הבנות מחייב (זיכרון דברים)."),
        2: ("חוק המתווכים - הגורם היעיל", "סוגיית הגורם היעיל בעסקת אקראי ללא הסכם בלעדיות."),
        3: ("חובת גילוי וניגוד עניינים", "מתווך בעל זיקה אישית לנכס (קרוב משפחה) שלא הצהיר על כך בכתב."),
        4: ("דמי תיווך בבלעדיות", "מכירה עצמית בתקופת הבלעדיות כאשר בוצעו פעולות שיווק."),
        5: ("תקנות האתיקה - הגינות וזהירות", "הסתרת מידע על פגמים נסתרים בנכס או תוכניות בנייה סמוכות."),
    }
    
    topic_info = topics_map.get(q_num, ("דיני מתווכים", f"מקרה בוחן מורכב מספר {q_num}"))
    
    # ייצור ה-JSON שיישמר ב-Buffer
    return {
        "q_id": f"REG_2026_{q_num}",
        "topic": topic_info[0],
        "question": f"{topic_info[1]} [תוכן השאלה מיוצר כאן ברמה של רשם המתווכים, כולל דקויות משפטיות משנת 2025]...",
        "options": {
            "1": "תשובה א' - מסיח משפטי קרוב",
            "2": "תשובה ב' - מבוססת על תקנות האתיקה",
            "3": "תשובה ג' - התשובה הנכונה לפי החוק",
            "4": "תשובה ד' - מסיח מורכב"
        },
        "correct": "3",
        "explanation": f"הסבר משפטי מעמיק המצטט את סעיפי חוק המתווכים ותקנות האתיקה הרלוונטיים ל{topic_info[0]}.",
        "difficulty": "קשה"
    }

# ---------------------------------------------------------
# Exam Logic & State Management
# ---------------------------------------------------------
def init_exam_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'explanation'
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 1
    if 'questions_buffer' not in st.session_state:
        st.session_state.questions_buffer = {}
    if 'active_questions' not in st.session_state:
        st.session_state.active_questions = set()
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

def run_app():
    init_exam_state()

    # שלב 1: עמוד הסבר
    if st.session_state.current_step == 'explanation':
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = registrar_question_factory(1)
            
        st.title("מבחן הסמכה רשמי - רשם המתווכים")
        st.write("המבחן מבוסס על חקיקה עדכנית (2025) ובחינות אמת מהשנתיים האחרונות.")
        
        if st.button("התחל בחינה"):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            # ייצור שאלה 2 ל-Buffer
            st.session_state.questions_buffer[2] = registrar_question_factory(2)
            st.rerun()

    # שלב 2: מהלך המבחן
    elif st.session_state.current_step == 'exam':
        # פריים ניווט (שמאל)
        with st.sidebar:
            st.subheader("ניווט שאלות")
            cols = st.columns(4)
            for i in range(1, 26):
                with cols[(i-1)%4]:
                    is_active = i in st.session_state.active_questions
                    label = f"**{i}**" if is_active else str(i)
                    if st.button(label, key=f"nav_{i}", disabled=not is_active):
                        st.session_state.current_question_idx = i
                        st.rerun()

        # הצגת השאלה
        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.info(f"נושא: {q_data['topic']}")
        st.markdown(f"### שאלה {q_idx}")
        st.write(q_data['question'])
        
        options = list(q_data['options'].values())
        st.radio("בחר את התשובה הנכונה ביותר:", options, key=f"ans_{q_idx}")

        # כפתורי התקדמות ולוגיקת Buffer (X+2)
        c1, c2 = st.columns(2)
        with c1:
            if q_idx > 1:
                if st.button("הקודם"):
                    st.session_state.current_question_idx -= 1
                    st.rerun()
        with c2:
            if q_idx < 25:
                if st.button("הבא"):
                    next_idx = q_idx + 1
                    st.session_state.current_question_idx = next_idx
                    st.session_state.active_questions.add(next_idx)
                    
                    # ייצור שאלה X+2 לתוך ה-Buffer
                    future_idx = next_idx + 1
                    if future_idx <= 25 and future_idx not in st.session_state.questions_buffer:
                        st.session_state.questions_buffer[future_idx] = registrar_question_factory(future_idx)
                    st.rerun()

if __name__ == "__main__":
    run_app()

# סוף קובץ
