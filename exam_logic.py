# ID: C-01
# Based on Anchor: 1218-G2

import streamlit as st
import time

def show_instructions():
    """מסך פתיחה עם המלל המדויק שביקשת"""
    st.title("📄 הוראות לבחינה")
    st.markdown("""
    ### הנחיות:
    * **מספר שאלות:** 25.
    * **זמן בחינה:** 3 דקות (לצורך הבדיקה).
    * **ניווט:** ניתן לעבור בין שאלות ולשנות תשובות.
    
    ---
    **שימו לב: המבחן יתחיל ברגע שתלחץ/י על כפתור התחל בחינה**
    """)
    
    # שינוי שם הכפתור לפי בקשתך
    if st.button("התחל בחינה"):
        st.session_state.start_time = time.time()
        st.session_state.step = 'exam'
        st.rerun()
