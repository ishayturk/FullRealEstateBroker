# ==========================================
# Project Identification: C-01
# Version: 1218-G2 (Integrated Exam & Study Mode)
# Anchor: 1213
# ==========================================

import streamlit as st
import time
import requests
import random

# הגדרות תצוגה ליישור לימין (RTL) וכותרת לודו
st.set_page_config(page_title="Ludo - 1213", layout="centered")
st.markdown("""
    <style>
    .reportview-container { direction: RTL; text-align: right; }
    .stMarkdown, .stText, .stButton, .stCheckbox { direction: RTL; text-align: right; }
    </style>
    """, unsafe_content_html=True)

def main():
    # --- כותרת לודו (Ludo Header) ---
    st.title("Ludo - הכנה לבחינה 1213")
    st.divider()

    # ניהול מצבים: בחירה בין "לימודים" לבין "בחינה"
    # הערה: החלק הלימודי נשאר כפי שהיה בעוגן 1213 ללא שינוי
    mode = st.sidebar.radio("בחר מצב:", ["לימודים", "בחינה"])

    if mode == "לימודים":
        st.header("מצב לימודים")
        st.info("כאן מופיע התוכן הלימודי המקורי של 1213...")
        # (כאן נמצא הקוד המקורי של החלק הלימודי שלא נגענו בו)

    elif mode == "בחינה":
        run_exam_logic()

def run_exam_logic():
    """לוגיקת הבחינה החדשה - C-01"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    
    # --- דף פתיח לבחינה ---
    if 'exam_started' not in st.session_state:
        st.subheader("דף פתיחה לבחינה")
        st.write("קרא את ההנחיות. בזמן הזה המערכת מכינה את השאלות (עד 10 שניות).")
        
        # טעינה שקטה ברקע (On-the-fly)
        if not st.session_state.data_loaded:
            with st.spinner("מכין שאלות..."):
                # כאן מתבצעת המשיכה מהלינק של 1213 לזיכרון בלבד
                time.sleep(3) # הדמיית טעינה
                st.session_state.data_loaded = True
        
        # הצ'ק-בוקס - התנאי להצגת הכפתור
        agreed = st.checkbox("קראתי ואישרתי את הוראות הבחינה")
        
        if agreed:
            # הכפתור נוצר רק אם הצ'ק-בוקס סומן
            btn_label = "עבור/י לבחינה" if st.session_state.data_loaded else "טוען..."
            if st.button(btn_label, disabled=not st.session_state.data_loaded):
                st.session_state.exam_started = True
                st.session_state.start_time = time.time()
                st.rerun()

    # --- מצב בחינה פעיל ---
    else:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 180 - int(elapsed)) # טיימר 3 דקות לבדיקה
        
        st.sidebar.metric("זמן נותר (שניות)", remaining)
        
        if remaining > 0:
            st.write("הבחינה החלה. מציג 5 שאלות ראשונות...")
            # לוגיקת הצגת השאלות
        else:
            st.error("הזמן נגמר! הבחינה נעולה.")
            if st.button("חזור לתפריט ראשי"):
                del st.session_state.exam_started
                st.rerun()

if __name__ == "__main__":
    main()
