import streamlit as st
import time
from logic import ExamManager  # ייבוא המחלקה מהקובץ השני

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

def apply_ui_fix():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], header {display: none !important;}
            .main .block-container {
                max-width: 800px !important;
                margin: 0 auto !important;
                padding-top: 80px !important;
            }
            .custom-timer {
                position: fixed; top: 0; left: 0; width: 100%; background: white;
                color: #ff4b4b; text-align: center; padding: 15px;
                font-size: 22px; font-weight: bold; border-bottom: 2px solid #ff4b4b;
                z-index: 9999;
            }
        </style>
    """, unsafe_allow_html=True)

# אתחול המנהל וטעינת הנתונים
manager = ExamManager()
exam_data = manager.load_exam()

apply_ui_fix()

if exam_data:
    # ניהול טיימר
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    remaining = max(0, (90 * 60) - (time.time() - st.session_state.start_time))
    mins, secs = divmod(int(remaining), 60)
    st.markdown(f'<div class="custom-timer">זמן נותר: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # הצגת תוכן המבחן
    instructions = exam_data.get('exam_info', {}).get('instructions', "")
    if instructions:
        st.info(instructions)

    for q in exam_data.get('questions', []):
        st.write(f"### שאלה {q['id']}")
        st.write(q['q'])
        st.radio("בחר תשובה:", q['o'], key=f"q_{q.get('id')}")
        st.divider()
else:
    st.error("שגיאה: לא הצלחתי לטעון את קבצי המבחן מתיקיית exams_data")
