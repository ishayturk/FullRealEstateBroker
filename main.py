import streamlit as st
import time

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    # הזרקת ה-CSS לביטול סיידבר, מרכוז 800px ועיצוב טיימר עליון
    st.markdown("""
        <style>
            /* הסתרת סיידבר וכותרות זבל */
            [data-testid="stSidebar"], section[data-testid="stSidebarNav"], header {
                display: none !important;
            }
            
            /* מרכוז תוכן ל-800px */
            .main .block-container {
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
            }

            /* טיימר צף מרכזי למעלה */
            .custom-timer-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background: white;
                border-bottom: 2px solid #e74c3c;
                text-align: center;
                padding: 10px 0;
                z-index: 1000;
                color: #e74c3c;
                font-size: 22px;
                font-weight: bold;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def render_exam_interface(exam_data):
    apply_ui_fix()
    
    # 1. ניהול זמן (90 דקות כפי שמופיע ב-JSON)
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(remaining), 60)
    
    # הצגת הטיימר המרכזי
    st.markdown(f'<div class="custom-timer-container">זמן נותר לבחינה: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # 2. הצגת הוראות בלבד (ללא כותרת ותאריך)
    if 'exam_info' in exam_data:
        st.info(exam_data['exam_info'].get('instructions', ""))

    # 3. הצגת השאלות
    for q in exam_data.get('questions', []):
        st.markdown(f"### שאלה {q['id']}")
        st.write(q['q'])
        st.radio("בחר תשובה:", q['o'], key=f"q_{q['id']}")
        st.divider()

    if st.button("הגש בחינה"):
        st.success("הבחינה הוגשה בהצלחה!")

# הערה: יש לוודא שהפונקציה render_exam_interface נקראת בתוך ה-Main של האפליקציה.
