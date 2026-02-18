import streamlit as st
import pandas as pd
import time
import os

# 1. הגדרות תצוגה ויישור לימין (RTL)
st.set_page_config(page_title="מערכת הכנה למתווכים", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# 2. אתחול משתני מצב (Session State)
if 'page' not in st.session_state: 
    st.session_state.page = 'home'
if 'answers' not in st.session_state: 
    st.session_state.answers = {}
if 'loaded_count' not in st.session_state: 
    st.session_state.loaded_count = 5

# 3. טעינת נתונים
@st.cache_data
def load_data():
    if os.path.exists("exam_data.csv"):
        return pd.read_csv("exam_data.csv")
    else:
        st.error("קובץ exam_data.csv לא נמצא במערכת")
        st.stop()

df = load_data()

# --- ניווט בין דפים ---

# דף הבית
if st.session_state.page == 'home':
    st.title("מערכת לימוד ובחינה")
    if st.button("📚 כניסה ללימודים"):
        st.session_state.page = 'study'
        st.rerun()
    if st.button("📝 התחלת בחינה"):
        st.session_state.page = 'exam'
        st.session_state.start_time = time.time()
        st.rerun()

# דף לימודים
elif st.session_state.page == 'study':
    st.title("מרכז לימודים")
    if st.button("חזרה לתפריט"):
        st.session_state.page = 'home'
        st.rerun()
    st.write("תוכן הלימודים יוצג כאן.")

# דף בחינה
elif st.session_state.page == 'exam':
    # ניהול זמן
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 180 - elapsed)
    st.sidebar.metric("⏳ זמן נותר", f"{int(remaining//60):02d}:{int(remaining%60):02d}")
    
    if remaining <= 0:
        st.session_state.page = 'results'
        st.rerun()

    # ניווט שאלות (Lazy Loading)
    q_num = st.sidebar.radio("בחר שאלה:", range(1, st.session_state.loaded_count + 1))
    q_idx = q_num - 1
    
    # הצגת השאלה
    row = df.iloc[q_idx]
    st.subheader(f"שאלה {q_num}")
    st.write(row['שאלה'])
    
    # בחירת תשובה
    options = ["1", "2", "3", "4"]
    saved_selection = st.session_state.answers.get(q_idx, None)
    
    ans = st.radio("תשובה:", options, 
                   index=options.index(saved_selection) if saved_selection in options else None,
                   key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = ans

    st.divider()
    
    # טעינת שאלות נוספות או הגשה
    if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
        if st.button("טען 5 שאלות נוספות"):
            st.session_state.loaded_count += 5
            st.rerun()
    elif st.session_state.loaded_count == 25:
        if st.button("סיים והגש בחינה"):
            st.session_state.page = 'results'
            st.rerun()

# דף תוצאות
elif st.session_state.page == 'results':
    st.title("סיכום בחינה")
    score = 0
    for i in range(25):
        u_ans = str(st.session_state.answers.get(i, "")).strip()
        c_ans = str(df.iloc[i]['תשובה_נכונה']).strip()
        if u_ans == c_ans:
            score += 1
    
    st.metric("ציון סופי", f"{int((score/25)*100)}/100")
    
    if st.button("חזרה לתפריט הראשי"):
        # איפוס נתוני הבחינה לסבב הבא
        for k in ['answers', 'loaded_count', 'start_time']:
            st.session_state.pop(k, None)
        st.session_state.page = 'home'
        st.rerun()
