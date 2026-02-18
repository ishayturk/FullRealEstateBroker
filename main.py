import streamlit as st
import pandas as pd
import time
import os

# הגדרות עמוד בסיסיות
st.set_page_config(page_title="מערכת הכנה למתווכים", layout="centered")

# CSS ליישור לימין ומניעת מריחת כפתורים
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    /* הגבלת רוחב כפתורים כדי שלא ימרחו */
    .stButton>button { width: auto; min-width: 150px; }
    </style>
    """, unsafe_allow_html=True)

# פונקציית טעינה
def load_data():
    if os.path.exists("exam_data.csv"):
        return pd.read_csv("exam_data.csv")
    else:
        st.error("קובץ הנתונים (exam_data.csv) חסר בשרת.")
        st.stop()

# ניהול מצבי סשן (מקור)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'loaded_count' not in st.session_state: st.session_state.loaded_count = 5

# --- דף כניסה (Login) ---
if not st.session_state.auth:
    st.title("כניסה למערכת")
    user_pass = st.text_input("קוד גישה", type="password")
    if st.button("התחבר"):
        if user_pass: # כאן ניתן להגדיר סיסמה ספציפית
            st.session_state.auth = True
            st.rerun()
    st.stop()

# טעינת נתונים לאחר כניסה
df = load_data()

# --- תפריט ראשי ---
if st.session_state.page == 'home':
    st.title("תפריט ראשי")
    if st.button("📚 לימודים"):
        st.session_state.page = 'study'
        st.rerun()
    if st.button("📝 בחינה"):
        st.session_state.page = 'exam'
        st.session_state.start_time = time.time()
        st.rerun()

# --- דף לימודים ---
elif st.session_state.page == 'study':
    st.title("חומרי לימוד")
    if st.button("חזרה"):
        st.session_state.page = 'home'
        st.rerun()
    st.write("תוכן הלימודים המקורי.")

# --- דף בחינה ---
elif st.session_state.page == 'exam':
    # טיימר מקורי
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 180 - elapsed)
    st.sidebar.metric("זמן", f"{int(remaining//60):02d}:{int(remaining%60):02d}")
    
    if remaining <= 0:
        st.session_state.page = 'results'
        st.rerun()

    # ניווט צדי
    q_num = st.sidebar.radio("שאלה:", range(1, st.session_state.loaded_count + 1))
    q_idx = q_num - 1
    
    # הצגת שאלה
    row = df.iloc[q_idx]
    st.subheader(f"שאלה {q_num}")
    st.write(row['שאלה'])
    
    # בחירת תשובה
    options = ["1", "2", "3", "4"]
    saved = st.session_state.answers.get(q_idx, None)
    ans = st.radio("תשובה:", options, 
                   index=options.index(saved) if saved in options else None,
                   key=f"q_{q_idx}")
    st.session_state.answers[q_idx] = ans

    # שליטה בשאלות (5 בכל פעם)
    st.write("---")
    if st.session_state.loaded_count < 25 and q_num == st.session_state.loaded_count:
        if st.button("טען עוד 5 שאלות"):
            st.session_state.loaded_count += 5
            st.rerun()
    elif st.session_state.loaded_count == 25:
        if st.button("הגש בחינה"):
            st.session_state.page = 'results'
            st.rerun()

# --- דף תוצאות ---
elif st.session_state.page == 'results':
    st.title("תוצאות")
    score = 0
    for i in range(25):
        u_ans = str(st.session_state.answers.get(i, "")).strip()
        c_ans = str(df.iloc[i]['תשובה_נכונה']).strip()
        if u_ans == c_ans: score += 1
    
    st.metric("ציון", f"{int((score/25)*100)}/100")
    if st.button("חזרה לתפריט"):
        for k in ['answers', 'loaded_count', 'start_time']: st.session_state.pop(k, None)
        st.session_state.page = 'home'
        st.rerun()
