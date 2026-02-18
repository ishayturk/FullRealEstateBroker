import streamlit as st
import pandas as pd
import time
import os

# הגדרות תצוגה ויישור לימין
st.set_page_config(page_title="מערכת בחינות", layout="wide")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# פונקציות ליבה
def load_data():
    if os.path.exists("exam_data.csv"):
        return pd.read_csv("exam_data.csv")
    else:
        st.error("קובץ exam_data.csv לא נמצא")
        st.stop()

# אתחול משתני סשן
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'loaded_count' not in st.session_state: st.session_state.loaded_count = 5

df = load_data()

# --- דף הבית ---
if st.session_state.page == 'home':
    col1, col2 = st.columns(2)
    if col1.button("📚 לימודים", use_container_width=True):
        st.session_state.page = 'study'
        st.rerun()
    if col2.button("📝 בחינה", use_container_width=True):
        st.session_state.page = 'exam'
        st.session_state.start_time = time.time()
        st.rerun()

# --- דף לימודים ---
elif st.session_state.page == 'study':
    if st.button("🔙 חזרה"):
        st.session_state.page = 'home'
        st.rerun()
    st.write("תוכן לימודי")

# --- דף בחינה ---
elif st.session_state.page == 'exam':
    # טיימר
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 180 - elapsed)
    st.sidebar.metric("⏳ זמן נותר", f"{int(remaining//60):02d}:{int(remaining%60):02d}")
    
    if remaining <= 0:
        st.session_state.page = 'results'
        st.rerun()

    # ניווט שאלות
    q_num = st.sidebar.radio("בחר שאלה:", range(1, st.session_state.loaded_count + 1))
    q_idx = q_num - 1
    
    # הצגת השאלה מהקובץ
    question_row = df.iloc[q_idx]
    st.subheader(f"שאלה {q_num}")
    st.write(question_row['שאלה'])
    
    # תשובות
    options = ["1", "2", "3", "4"]
    current_selection = st.session_state.answers.get(q_idx, None)
    
    ans = st.radio("תשובה:", options, 
                   index=options.index(current_selection) if current_selection in options else None,
                   key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = ans

    # שליטה בטעינה וסיום
    st.divider()
    if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
        if st.button("טען 5 שאלות נוספות"):
            st.session_state.loaded_count += 5
            st.rerun()
    elif st.session_state.loaded_count == 25:
        if st.button("סיום והגשה"):
            st.session_state.page = 'results'
            st.rerun()

# --- דף תוצאות ---
elif st.session_state.page == 'results':
    st.title("תוצאות הבחינה")
    score = 0
    for i in range(25):
        user_ans = str(st.session_state.answers.get(i, "")).strip()
        correct_ans = str(df.iloc[i]['תשובה_נכונה']).strip()
        if user_ans == correct_ans:
            score += 1
    
    st.metric("ציון סופי", f"{int((score/25)*100)}/100")
    
    if st.button("חזרה לתפריט"):
        for k in ['answers', 'loaded_count', 'start_time']: 
            st.session_state.pop(k, None)
        st.session_state.page = 'home'
        st.rerun()
