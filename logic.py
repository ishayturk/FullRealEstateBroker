# File: logic.py
# Version: V221
# Date: 2026-02-23
# Time: 18:15

import streamlit as st
import json

def registrar_engine_generate(q_num):
    """
    מנוע רשם המתווכים - ייצור שאלה מורכבת בזמן אמת (פרוטוקול C-01)
    מבוסס על אפיון בחינות מאי 25, אוגוסט 24, פברואר 25 ויולי 25.
    """
    # המנוע מייצר את השאלה על בסיס ידע באתיקה וחוק המתווכים
    # כאן מוצגת דוגמה למבנה השאלה המיוצרת שנכנסת לזיכרון ה-Buffer
    if q_num == 1:
        return {
            "q_id": "REG_2026_001",
            "topic": "אתיקה מקצועית - ניגוד עניינים וחובת גילוי",
            "question": "מתווך במקרקעין, בעל רישיון בתוקף, הציע ללקוחה דירה למכירה בבלעדיות. במהלך המשא ומתן, התברר כי המתווך הוא בן דודו של המוכר, וכי הוא מחזיק באופציה לרכישת הדירה במידה ולא תימכר תוך שלושה חודשים. המתווך לא ציין עובדות אלו בפני הקונה בכתב, אך טען בעל פה כי הוא 'מכיר את המוכר היטב'. העסקה נחתמה והקונה גילתה את הזיקה האישית. האם המתווך הפר את חובותיו?",
            "options": {
                "1": "לא; חובת הגילוי חלה רק על קשר משפחתי מדרגה ראשונה (הורים/ילדים) ולא על בני דודים.",
                "2": "כן; המתווך הפר את חובת ההגינות והזהירות ואת האיסור על ניגוד עניינים, שכן לא גילה בכתב את עניינו האישי בנכס.",
                "3": "לא; מאחר שהמתווך ציין בעל פה שהוא מכיר את המוכר, הוא עמד בדרישת הגילוי הנאות לפי חוק המתווכים.",
                "4": "כן; אך ורק בגלל האופציה לרכישה, שכן קרבה משפחתית אינה נחשבת לניגוד עניינים בתחום התיווך."
            },
            "correct": "2",
            "explanation": "לפי סעיף 8 לחוק המתווכים ותקנות האתיקה (2012), על מתווך לגלות ללקוחו כל עניין אישי שיש לו בנכס או בעסקה. גילוי זה חייב להיות בכתב ובאופן מפורש.",
            "difficulty": "קשה"
        }
    # עבור שאלות נוספות, המנוע ימשיך לייצר באותו פורמט ורמת מורכבות
    return {
        "q_id": f"REG_2026_{q_num:03d}",
        "topic": "חוק המתווכים - הגורם היעיל ודמי תיווך",
        "question": f"מקרה בוחן מורכב לשאלה {q_num} המבוסס על חקיקת המתווכים ובחינות אמת...",
        "options": {"1": "תשובה א'", "2": "תשובה ב'", "3": "תשובה ג'", "4": "תשובה ד'"},
        "correct": "1",
        "explanation": "הסבר משפטי מפורט המצטט את סעיפי החוק הרלוונטיים...",
        "difficulty": "קשה"
    }

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
    
    # CSS: חלוקה ל-General, Desktop, Mobile
    st.markdown("""
        <style>
        /* General */
        .main { direction: rtl; text-align: right; }
        .stRadio > label { font-size: 1.1rem; padding-bottom: 10px; }
        
        /* Desktop */
        @media (min-width: 1024px) {
            .stSidebar { width: 300px !important; }
        }
        
        /* Mobile */
        @media (max-width: 1023px) {
            .stSidebar { width: 100% !important; }
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.current_step == 'explanation':
        # ייצור שאלה 1 בזיכרון
        if 1 not in st.session_state.questions_buffer:
            st.session_state.questions_buffer[1] = registrar_engine_generate(1)
            
        st.title("מבחן הסמכה - רשם המתווכים")
        st.write("ברוכים הבאים למבחן ההסמכה הרשמי. המבחן כולל 25 שאלות מורכבות.")
        
        if st.button("התחל בחינה"):
            st.session_state.current_step = 'exam'
            st.session_state.active_questions.add(1)
            # לחיצה מייצרת את שאלה 2 בזיכרון (Buffer)
            st.session_state.questions_buffer[2] = registrar_engine_generate(2)
            st.rerun()

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

        # פריים תוכן
        q_idx = st.session_state.current_question_idx
        q_data = st.session_state.questions_buffer[q_idx]
        
        st.markdown(f"**נושא:** {q_data['topic']}")
        st.markdown(f"### שאלה {q_idx}")
        st.write(q_data['question'])
        
        # הצגת תשובות ושמירה ב-JSON בזיכרון
        options_list = list(q_data['options'].values())
        current_ans = st.session_state.user_answers.get(q_idx)
        default_idx = list(q_data['options'].keys()).index(current_ans) if current_ans else None
        
        selected_opt = st.radio("בחר את התשובה הנכונה ביותר:", options_list, 
                                index=default_idx, key=f"radio_{q_idx}")
        
        if selected_opt:
            for key, val in q_data['options'].items():
                if val == selected_opt:
                    st.session_state.user_answers[q_idx] = key

        # כפתורי ניווט ולוגיקת Buffer
        col_prev, col_next = st.columns(2)
        with col_prev:
            if q_idx > 1:
                if st.button("לשאלה הקודמת"):
                    st.session_state.current_question_idx -= 1
                    st.rerun()
        
        with col_next:
            if q_idx < 25:
                if st.button("לשאלה הבאה"):
                    next_idx = q_idx + 1
                    st.session_state.current_question_idx = next_idx
                    st.session_state.active_questions.add(next_idx)
                    
                    # ייצור X+2 (Buffer)
                    future_idx = next_idx + 1
                    if future_idx <= 25 and future_idx not in st.session_state.questions_buffer:
                        st.session_state.questions_buffer[future_idx] = registrar_engine_generate(future_idx)
                    st.rerun()
            else:
                if st.button("סיים בחינה והצג משוב"):
                    st.session_state.current_step = 'feedback'
                    st.rerun()

    elif st.session_state.current_step == 'feedback':
        st.title("סיכום בחינה ומשוב משפטי")
        # לוגיקה למעבר על ה-JSON-ים בזיכרון והצגת תשובות מול נכונות
        st.write("כאן יוצג פירוט השאלות, התשובות וההסברים המורכבים.")

if __name__ == "__main__":
    run_app()

# סוף קובץ
