# ==========================================
# Project Identification: C-01
# Version: 1218-G2 (Integrated Exam Mode)
# Anchor: 1213
# Description: Streamlit main file with on-the-fly exam loading
# ==========================================

import streamlit as st
import time
import requests
import random

def init_exam_session():
    """אתחול משתני סשן לבחינה - C-01"""
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'exam_ready' not in st.session_state:
        st.session_state.exam_ready = False
    if 'current_exam_id' not in st.session_state:
        st.session_state.current_exam_id = None
    if 'used_exams' not in st.session_state:
        st.session_state.used_exams = []

def load_exam_on_the_fly():
    """משיכת מועד אקראי מהמקור - לזיכרון בלבד"""
    # כאן תבוא הכתובת של המקור שסיפקת
    SOURCE_URL = "https://raw.githubusercontent.com/user/repo/main/exams_index.json"
    
    try:
        # 1. משיכת רשימת המועדים (בזמן שהמשתמש קורא)
        # בתרחיש אמת: requests.get(SOURCE_URL)
        
        # הדמיית הגרלה מתוך רשימה (מוודא שלא חוזר על עצמו באותו סשן)
        all_exams = ["Spring_2024_1", "Spring_2024_2", "Summer_2023_1"]
        available = [e for e in all_exams if e not in st.session_state.used_exams]
        
        if not available:
            st.session_state.used_exams = [] # איפוס אם נגמרו המועדים
            available = all_exams
            
        chosen_exam = random.choice(available)
        st.session_state.current_exam_id = chosen_exam
        st.session_state.used_exams.append(chosen_exam)
        
        # 2. הבאת 5 שאלות ראשונות לזיכרון
        # Simulation of fetching actual questions
        time.sleep(3) # זמן טעינה (עד 10 שניות לפי התכנון)
        
        st.session_state.data_loaded = True
        st.session_state.exam_ready = True
    except Exception as e:
        st.error(f"שגיאה בטעינת המבחן: {e}")

def main():
    init_exam_session()
    
    st.title("מערכת בחינות - 1213")
    st.subheader("C-01 | גרסה 1218-G2")
    
    # --- דף פתיח ---
    if 'start_time' not in st.session_state:
        st.info("קרא את ההנחיות בעיון לפני המעבר לבחינה.")
        st.write("1. לרשותך 3 דקות (גרסת בדיקה).")
        st.write("2. לאחר הלחיצה על 'עבור/י לבחינה', הטיימר יתחיל לפעול.")
        
        # התחלת טעינה שקטה ברקע
        if not st.session_state.data_loaded:
            load_exam_on_the_fly()
        
        # הצ'ק-בוקס - התנאי להופעת הכפתור
        agreed = st.checkbox("קראתי ואישרתי")
        
        if agreed:
            # הכפתור מופיע, אך פעיל רק אם הטעינה הסתיימה
            button_label = "עבור/י לבחינה" if st.session_state.exam_ready else "טוען נתונים..."
            if st.button(button_label, disabled=not st.session_state.exam_ready):
                st.session_state.start_time = time.time()
                st.rerun()
                
    # --- מצב בחינה פעיל ---
    else:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 180 - int(elapsed)) # טיימר 3 דקות (180 שניות)
        
        if remaining > 0:
            st.sidebar.metric("זמן נותר (שניות)", remaining)
            st.write(f"מציג שאלות ממועד: {st.session_state.current_exam_id}")
            # כאן תבוא לוגיקת הצגת השאלות (5 בכל פעם)
        else:
            st.error("זמן הבחינה הסתיים!")
            st.button("סיים/י בחינה וראה תוצאות")

if __name__ == "__main__":
    main()
