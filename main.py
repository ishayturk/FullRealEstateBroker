import streamlit as st
import pandas as pd
import time
import os
import random
from exam_logic import get_unique_exam, prepare_question_data
from ui_utils import show_instructions, render_navigation, show_results_summary

# הגדרות עמוד ויישור לימין (RTL) - חובה להרצה תקינה בעברית
st.set_page_config(page_title="פורטל הכנה למתווכים", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# אתחול מצב אפליקציה - ברירת מחדל לתפריט ראשי
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'
if 'finished_exams' not in st.session_state:
    st.session_state.finished_exams = []

# טעינת נתונים
@st.cache_data
def load_data():
    if not os.path.exists("exam_data.csv"):
        # יצירת נתונים בסיסיים אם הקובץ חסר
        data = {
            'שאלה': [f'שאלת נדל"ן מספר {i}' for i in range(1, 26)],
            'מועד_א': [str(random.randint(1, 4)) for _ in range(25)],
            'תשובה_נכונה': ["1"] * 25
        }
        pd.DataFrame(data).to_csv("exam_data.csv", index=False, encoding='utf-8-sig')
    return pd.read_csv("exam_data.csv")

df = load_data()

# --- ניהול דפי המערכת ---

# 1. תפריט ראשי
if st.session_state.page == 'main_menu':
    st.title("🏠 תפריט ראשי - הכנה למבחן המתווכים")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 שיעורים ולימודים", use_container_width=True):
            st.session_state.page = 'study'
            st.rerun()
    with col2:
        if st.button("📝 התחל בחינה חדשה", use_container_width=True):
            st.session_state.page = 'exam'
            st.session_state.step = 'instructions'
            st.rerun()

# 2. דף לימודים
elif st.session_state.page == 'study':
    st.title("📚 מרכז לימודים")
    if st.button("🔙 חזרה לתפריט"):
        st.session_state.page = 'main_menu'
        st.rerun()
    st.divider()
    st.write("כאן מופיעים חומרי הלימוד והשיעורים שלך.")

# 3. דף בחינה
elif st.session_state.page == 'exam':
    # לוגיקת בחינה מלאה
    if st.session_state.step == 'instructions':
        if 'current_exam_col' not in st.session_state:
            st.session_state.current_exam_col = get_unique_exam(df, st.session_state.finished_exams)
        
        if st.session_state.current_exam_col:
            show_instructions()
            if st.button("בטל וחזור לתפריט"):
                st.session_state.page = 'main_menu'
                st.rerun()
        else:
            st.warning("לא נותרו מבחנים חדשים בסשן זה.")
            if st.button("חזרה לתפריט"):
                st.session_state.page = 'main_menu'
                st.rerun()

    elif st.session_state.step == 'exam':
        # הפעלת מנוע הבחינה (מזהה C-01)
        if 'current_exam_data' not in st.session_state or st.session_state.current_exam_data is None:
            st.session_state.current_exam_data = prepare_question_data(df, st.session_state.current_exam_col, 0, 25)
        
        # ניהול זמן
        elapsed = time.time() - st.session_state.start_time
        rem = max(0, 180 - elapsed)
        st.sidebar.metric("⏳ זמן נותר", f"{int(rem//60):02d}:{int(rem%60):02d}")
        
        if rem <= 0:
            st.session_state.step = 'results'
            st.rerun()

        # ניווט וטעינה מדורגת
        q_num = render_navigation(st.session_state.loaded_count, st.sidebar.toggle("נייד"))
        q_idx = q_num - 1
        
        st.subheader(f"שאלה {q_num} | {st.session_state.current_exam_col}")
        st.write(st.session_state.current_exam_data[q_idx]['שאלה'])
        
        # תשובות
        opts = ["1", "2", "3", "4"]
        ans = st.radio("בחר תשובה:", opts, 
                       index=opts.index(st.session_state.answers[q_idx]) if q_idx in st.session_state.answers else None,
                       key=f"q_{q_idx}")
        st.session_state.answers[q_idx] = ans

        st.divider()
        if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
            if st.button("טען עוד 5 שאלות"):
                st.session_state.loaded_count += 5
                st.rerun()
        elif st.session_state.loaded_count == 25:
            if st.button("סיום והגשה"):
                st.session_state.finished_exams.append(st.session_state.current_exam_col)
                st.session_state.step = 'results'
                st.rerun()

    elif st.session_state.step == 'results':
        show_results_summary(st.session_state.answers, st.session_state.current_exam_data)
        if st.button("חזרה לתפריט הראשי"):
            for k in ['current_exam_col', 'answers', 'loaded_count', 'start_time', 'current_exam_data']:
                st.session_state.pop(k, None)
            st.session_state.page = 'main_menu'
            st.rerun()
