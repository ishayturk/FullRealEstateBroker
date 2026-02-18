# ==========================================
# Project Identification: C-01
# Version: 1218-G4 (Stable Production)
# Anchor: 1213
# ==========================================

import streamlit as st
import time
import random

# הגדרות דף בסיסיות
st.set_page_config(page_title="Ludo - 1213", layout="centered")

# פונקציה ליישור לימין (CSS פשוט ויציב)
st.markdown("""
    <style>
    .stApp { direction: RTL; text-align: right; }
    </style>
    """, unsafe_content_html=True)

def main():
    # אתחול משתני סשן
    if 'page_state' not in st.session_state:
        st.session_state.page_state = 'home'
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    # כותרת לודו קבועה
    st.title("Ludo - 1213")
    st.divider()

    # --- תצוגת דף הבית (מסך כניסה) ---
    if st.session_state.page_state == 'home':
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📚 כניסה ללימודים", use_container_width=True):
                st.session_state.page_state = 'study'
                st.rerun()
        
        with col2:
            if st.button("📝 כניסה לבחינה", use_container_width=True):
                st.session_state.page_state = 'exam_intro'
                st.rerun()

    # --- דף פתיח לבחינה (C-01) ---
    elif st.session_state.page_state == 'exam_intro':
        st.header("הנחיות לבחינה")
        st.write("בזמן קריאת ההנחיות, המערכת מכינה את השאלות בזיכרון (עד 10 שניות).")
        st.info("זמן בחינה: 3 דקות (גרסת בדיקה).")

        # טעינה שקטה ברקע
        if not st.session_state.data_loaded:
            with st.spinner("טוען נתונים מהמאגר..."):
                time.sleep(4) # הדמיית משיכה והגרלה מ-1213
                st.session_state.data_loaded = True
                st.rerun()

        # הצ'ק-בוקס
        agreed = st.checkbox("קראתי ואישרתי את ההנחיות")

        # כפתור מעבר - מופיע ופעיל רק לפי התנאים
        if agreed:
            if st.button("עבור/י לבחינה", disabled=not st.session_state.data_ready if 'data_ready' in st.session_state else not st.session_state.data_loaded):
                st.session_state.page_state = 'exam_active'
                st.session_state.start_time = time.time()
                st.rerun()
        
        if st.button("חזרה"):
            st.session_state.page_state = 'home'
            st.rerun()

    # --- מצב לימודים (חלק לימודי מקורי) ---
    elif st.session_state.page_state == 'study':
        st.header("מצב לימודים")
        st.write("כאן מופיע התוכן הלימודי המקורי של 1213.")
        if st.button("חזרה לתפריט"):
            st.session_state.page_state = 'home'
            st.rerun()

    # --- מצב בחינה פעיל ---
    elif st.session_state.page_state == 'exam_active':
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 180 - int(elapsed)) # 3 דקות = 180 שניות
        
        st.subheader(f"זמן נותר: {remaining} שניות")
        
        if remaining > 0:
            st.write("הבחינה בשימוש. מציג 5 שאלות ראשונות...")
            # כאן תרוץ לוגיקת השאלות
            if st.button("סיום בחינה"):
                st.session_state.page_state = 'home'
                st.session_state.data_loaded = False
                st.rerun()
        else:
            st.error("הזמן הסתיים. הבחינה נעולה.")
            if st.button("חזרה לתפריט"):
                st.session_state.page_state = 'home'
                st.session_state.data_loaded = False
                st.rerun()

if __name__ == "__main__":
    main()
