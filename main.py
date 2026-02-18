import streamlit as st
import time

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    # הזרקת CSS מתוקן - מוודא שהתוכן המרכזי גלוי
    st.markdown("""
        <style>
            /* העלמת סיידבר וכותרות מערכת */
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], header {
                display: none !important;
            }
            
            /* הצגת התוכן המרכזי ומרכוזו */
            .main .block-container {
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
                display: block !important;
            }

            /* עיצוב טיימר צף עליון */
            .custom-timer {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: white;
                color: #ff4b4b;
                text-align: center;
                padding: 15px;
                font-size: 22px;
                font-weight: bold;
                border-bottom: 2px solid #ff4b4b;
                z-index: 9999;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def render_exam_interface(exam_data):
    # הפעלת התיקון העיצובי
    apply_ui_fix()
    
    # בדיקה אם יש נתונים - אם אין, נציג הודעה במקום מסך ריק
    if not exam_data or 'questions' not in exam_data:
        st.error("לא נמצאו נתונים לבחינה. אנא וודא שקובץ ה-JSON תקין.")
        return

    # ניהול טיימר
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, (90 * 60) - elapsed)
    mins, secs = divmod(int(remaining), 60)
    
    # הצגת הטיימר
    st.markdown(f'<div class="custom-timer">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # הצגת הוראות
    instructions = exam_data.get('exam_info', {}).get('instructions', "")
    if instructions:
        st.info(instructions)
    
    # הצגת השאלות
    for q in exam_data.get('questions', []):
        st.markdown(f"### שאלה {q['id']}")
        st.write(q['q'])
        st.radio("בחר תשובה:", q['o'], key=f"q_{q['id']}")
        st.divider()

    if st.button("הגש בחינה"):
        st.success("הבחינה הוגשה בהצלחה!")
