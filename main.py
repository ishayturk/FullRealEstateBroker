# File: main.py
# Version: V229
# Date: 2026-02-23
# Time: 19:55

import streamlit as st

# הגדרות עמוד - עוגן 1213
st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------
# CSS Section - חלוקה ל-3 חלקים (General, Desktop, Mobile)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. General Section */
    .main { direction: rtl; text-align: right; }
    [data-testid="stHeader"] { display: none; }
    .stRadio > label { font-weight: bold; }
    
    /* הסטריפ העליון - עיצוב V38 */
    .top-strip {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: #ffffff;
        border-bottom: 1px solid #eeeeee;
        margin-top: 10px;
    }
    .main-menu-link { color: #007bff; text-decoration: none; font-weight: bold; cursor: pointer; }
    
    /* 2. Desktop Section */
    @media (min-width: 1024px) {
        .main-content { max-width: 1200px; margin: 0 auto; padding: 2rem; }
    }
    
    /* 3. Mobile Section */
    @media (max-width: 1023px) {
        .main-content { padding: 0.5rem; }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Registrar Engine - מנוע ייצור השאלות (C-01)
# ---------------------------------------------------------
def registrar_question_factory(q_num):
    """ייצור שאלה מורכבת בזמן אמת - תיווך בלבד"""
    topics_map = {
        1: ("אתיקה - איסור פעולה משפטית", "מתווך שסייע בעריכת מסמך משפטי בניגוד לסעיף 12."),
        2: ("חוק המתווכים - הגורם היעיל", "סוגיית הגורם היעיל בעסקה ללא בלעדיות."),
    }
    topic_data = topics_map.get(q_num, ("דיני תיווך", f"מקרה בוחן מורכב {q_num}"))
    return {
        "q_id": f"REG_{q_num}",
        "topic": topic_data[0],
        "question": f"{topic_data[1]} [תוכן השאלה ברמת רשם המתווכים]...",
        "options": {"1": "תשובה א'", "2": "תשובה ב'", "3": "התשובה הנכונה", "4": "תשובה ד'"},
        "correct": "3",
        "explanation": "הסבר משפטי מפורט...",
        "difficulty": "קשה"
    }

# ---------------------------------------------------------
# Session State Init
# ---------------------------------------------------------
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'explanation'
if 'questions_buffer' not in st.session_state:
    st.session_state.questions_buffer = {}
if 'active_questions' not in st.session_state:
    st.session_state.active_questions = set()
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 1
if 'user_name' not in st.session_state:
    st.session_state.user_name = "ישראל ישראלי"

# ---------------------------------------------------------
# UI Components
# ---------------------------------------------------------
def render_top_strip():
    """הסטריפ העליון עם הלינק 'לתפריט הראשי'"""
    cols = st.columns([1, 2, 1])
    with cols[0]:
        st.markdown('<a href="#" class="main-menu-link">לתפריט הראשי</a>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div style="text-align: center; font-size: 1.2rem; font-weight: bold;">{st.session_state.user_name}</div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div style="text-align: left; font-weight: bold;">לוגו מתווך בקליק</div>', unsafe_allow_html=True)
    st.markdown('<hr style="margin-top: 5px; margin-bottom: 20px;">', unsafe_allow_html=True)

def run_app():
    render_top_strip()
    
    # שלב עמוד ההסבר
    if st.session_state.current_step == 'explanation':
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = registrar_question_factory(1)
            
        st.title("הסבר על הבחינה")
        st.write("ברוכים הבאים למערכת התרגול. יש לקרוא את ההוראות ולאשרן.")
        
        # צ'קבוקס ועימוד V38
        confirmed = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל בבחינה")
        
        if st.button("עבור לבחינה", disabled=not confirmed):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            st.session_state.questions_buffer[2] = registrar_question_factory(2)
            st.rerun()

    # שלב המבחן
    elif st.session_state.current_step == 'exam':
        with st.sidebar:
            st.subheader("ניווט")
            sidebar_cols = st.columns(4)
            for i in range(1, 26):
                with sidebar_cols[(i-1)%4]:
                    is_active = i in st.session_state.active_questions
                    btn_label = f"**{i}**" if is_active else str(i)
                    if st.button(btn_label, key=f"nav_{i}", disabled=not is_active):
                        st.session_state.current_question_idx = i
                        st.rerun()

        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.info(f"נושא: {q_data['topic']}")
        st.markdown(f"### שאלה {q_idx}")
        st.write(q_data['question'])
        st.radio("בחר תשובה:", list(q_data['options'].values()), key=f"ans_{q_idx}")

        if st.button("הבא"):
            if q_idx < 25:
                next_idx = q_idx + 1
                st.session_state.current_question_idx = next_idx
                st.session_state.active_questions.add(next_idx)
                
                future_idx = next_idx + 1
                if future_idx <= 25 and future_idx not in st.session_state.questions_buffer:
                    st.session_state.questions_buffer[future_idx] = registrar_question_factory(future_idx)
                st.rerun()

if __name__ == "__main__":
    run_app()

# סוף קובץ
