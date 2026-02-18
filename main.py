# ==========================================
# Project Identification: C-01
# Version: 1218-G2 (Stable)
# Anchor: 1213
# ==========================================

import streamlit as st
import time

# 1. הגדרות דף - חייב להיות בראש הקובץ
st.set_page_config(page_title="Ludo - 1213", layout="centered")

def main():
    # כותרת לודו
    st.title("Ludo - 1213")
    
    # ניהול מצבים בסרגל הצד (ימינה/שמאלה אוטומטי ב-Streamlit)
    mode = st.sidebar.radio("תפריט", ["לימודים", "בחינה"])

    if mode == "לימודים":
        st.header("מצב לימודים")
        st.write("כאן התוכן הלימודי המקורי.")
        # הקוד הלימודי המקורי שלך כאן

    elif mode == "בחינה":
        run_exam_module()

def run_exam_module():
    # אתחול משתנים בזיכרון (Session State)
    if 'data_ready' not in st.session_state:
        st.session_state.data_ready = False
    
    # דף פתיחה
    if 'active_exam' not in st.session_state:
        st.subheader("הנחיות לבחינה")
        st.write("בזמן הקריאה המערכת טוענת את המבחן (3 דקות לגרסת בדיקה).")

        # טעינה שקטה ברקע
        if not st.session_state.data_ready:
            with st.spinner("טוען..."):
                time.sleep(3) # הדמיית טעינה מהלינק
                st.session_state.data_ready = True
                st.rerun()

        # הצ'ק-בוקס שלך
        agreed = st.checkbox("קראתי ואישרתי")

        # הכפתור מופיע רק אם סימנו V
        if agreed:
            # הכפתור פעיל רק אם הטעינה הסתיימה
            if st.button("עבור/י לבחינה", disabled=not st.session_state.data_ready):
                st.session_state.active_exam = True
                st.session_state.start_time = time.time()
                st.rerun()

    # מצב בחינה פעיל
    else:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 180 - int(elapsed)) # 3 דקות

        st.sidebar.metric("זמן נותר", f"{remaining} שניות")

        if remaining > 0:
            st.write("הבחינה החלה.")
            if st.button("סיים בחינה"):
                del st.session_state.active_exam
                st.rerun()
        else:
            st.error("הזמן נגמר.")
            if st.button("חזרה לתפריט"):
                del st.session_state.active_exam
                st.rerun()

if __name__ == "__main__":
    main()
