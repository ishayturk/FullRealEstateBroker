# Version: 1218-G4
# Anchor: 1218-G2
# Description: RTL Support, Accumulative Memory (5-25), Random Exam Selection, Page-Load Trigger.

import streamlit as st
import json
import os
import random

# הגדרות עמוד
st.set_page_config(page_title="מבחן מתווכים", layout="wide", initial_sidebar_state="collapsed")

# הזרקת CSS ליישור לימין (RTL) וניקוי ממשק
st.markdown("""
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    h1, h2, h3, p, span, label, .stMarkdown {
        text-align: right !important;
        direction: RTL !important;
    }
    /* עיצוב הצ'קבוקס */
    .stCheckbox {
        margin-top: 25px;
        margin-bottom: 20px;
    }
    /* כפתור מעבר לבחינה */
    div.stButton > button {
        width: 200px;
        height: 45px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session():
    """מפעיל את הלוגיקה בטעינה הראשונה של הפריים"""
    if 'page' not in st.session_state:
        st.session_state.page = 'explanation'
        st.session_state.current_q_idx = 0
        st.session_state.user_answers = {}
        st.session_state.loaded_questions = []
        st.session_state.full_exam_data = []
        st.session_state.exam_ready = False
        
        # בחירת מבחן אקראי
        all_files = [f for f in os.listdir('.') if f.endswith('.json')]
        if all_files:
            selected_file = random.choice(all_files)
            try:
                with open(selected_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    st.session_state.full_exam_data = data.get('questions', [])
                    # טעינה ראשונית של 5 שאלות
                    st.session_state.loaded_questions = st.session_state.full_exam_data[:5]
                    st.session_state.exam_ready = True
            except:
                st.session_state.exam_ready = False

def main():
    initialize_session()

    # --- עמוד הסבר ---
    if st.session_state.page == 'explanation':
        st.title("ראשית - מבחן לרשיון מתווך בישראל")
        st.subheader("אנא קרא/י את הוראות הבחינה")
        
        st.write("• משך הבחינה הוא 90 דקות.")
        st.write("• בבחינה 25 שאלות שנבחרו עבורך באופן אקראי.")
        st.write("• המעבר בין השאלות הוא ליניארי - יש לענות על שאלה כדי להתקדם.")
        st.write("• לא ניתן לחזור לשאלות קודמות או לדלג.")

        # בזמן שהוא קורא, נטען עוד 5 שאלות (Buffer של 10 סה"כ)
        if st.session_state.exam_ready and len(st.session_state.loaded_questions) < 10:
            st.session_state.loaded_questions = st.session_state.full_exam_data[:10]

        st.write("") 
        agreed = st.checkbox("קראתי את ההוראות ואני מוכן/ה להתחיל")
        
        if st.button("מעבר לבחינה"):
            if not st.session_state.exam_ready:
                st.error("שגיאה: לא נמצאו קבצי בחינה תקינים במערכת.")
            elif agreed:
                st.session_state.page = 'exam'
                st.rerun()
            else:
                st.error("יש לאשר את קריאת ההוראות.")

    # --- עמוד הבחינה ---
    elif st.session_state.page == 'exam':
        idx = st.session_state.current_q_idx
        questions = st.session_state.loaded_questions
        
        # לוגיקת צבירה (Buffer): בכל שאלה שהיא כפולה של 5, טוענים את ה-5 הבאות
        if (idx + 1) % 5 == 0 and len(questions) < 25:
            next_limit = len(questions) + 5
            st.session_state.loaded_questions = st.session_state.full_exam_data[:next_limit]

        if idx < len(questions):
            q = questions[idx]
            st.header(f"שאלה {idx + 1}")
            st.write(q['question'])
            
            # הצגת תשובה קודמת אם קיימת בזיכרון
            current_ans = st.session_state.user_answers.get(idx, None)
            choice = st.radio("בחר/י תשובה:", q['options'], index=None, key=f"q_{idx}")
            
            st.divider()
            
            is_last = (idx == 24)
            if st.button("סיום והגשה" if is_last else "לשאלה הבאה"):
                if choice:
                    st.session_state.user_answers[idx] = choice
                    if not is_last:
                        st.session_state.current_q_idx += 1
                        st.rerun()
                    else:
                        st.session_state.page = 'results'
                        st.rerun()
                else:
                    st.error("חובה לסמן תשובה.")

if __name__ == "__main__":
    main()
