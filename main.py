import streamlit as st
from logic import ExamManager
import time

# ID: C-01 | Anchor: 1213 | Version: 1218-G2

st.set_page_config(page_title="מבחן רישוי למתווכים", layout="wide")

# עיצוב RTL ויישור לימין
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[role="radiogroup"] { direction: rtl; text-align: right; }
    .stButton button { width: 100%; background-color: #4CAF50; color: white; }
    .info-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-right: 5px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

exam = ExamManager()

# ניהול מסכים: עמוד פתיחה / מבחן פעיל
if 'exam_started' not in st.session_state:
    st.title("מבחן רישוי למתווכים")
    
    if exam.load_exam_from_json():
        info = st.session_state.full_exam_data['exam_info']
        
        # הסבר על הבחינה
        st.markdown(f"""
        <div class="info-box">
            <h3>ברוכים הבאים לבחינת התרגול</h3>
            <p><b>מידע על הבחינה:</b> {info['instructions']}</p>
            <p>• הבחינה כוללת 25 שאלות.</p>
            <p>• בכל שלב יוצגו 5 שאלות חדשות (לוגיקת 5-5-5).</p>
            <p>• משך הבחינה המומלץ: 120 דקות.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # מרווח
        
        # צ'ק-בוקס לאישור התקנון
        agreed = st.checkbox("אני מאשר/ת שקראתי את ההוראות ואני מוכן/ה להתחיל בבחינה.")
        
        if not st.session_state.questions:
            exam.fetch_batch(0) # טעינה שקטה של 5 שאלות ראשונות
            
        # כפתור כניסה - פעיל רק אם הצ'קבוקס מסומן
        if st.button("כניסה למבחן", disabled=not agreed):
            st.session_state.exam_started = True
            st.session_state.current_q_idx = 0
            st.session_state.start_time = time.time()
            st.rerun()
else:
    # ממשק הבחינה הפעיל (שאלות וניווט)
    q_idx = st.session_state.current_q_idx
    questions = st.session_state.questions
    
    # טיימר בסידבר
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, (exam.time_limit * 60) - elapsed)
    st.sidebar.metric("זמן נותר", f"{remaining // 60}:{remaining % 60:02d}")
    
    if q_idx < len(questions):
        q_data = questions[q_idx]
        st.subheader(f"שאלה {q_idx + 1} מתוך {exam.total_questions}")
        st.info(q_data['q'])
        
        st.radio("בחר את התשובה הנכונה:", q_data['o'], key=f"q_{q_idx}")
        
        col1, col2 = st.columns(2)
        with col1:
            if q_idx > 0 and st.button("שאלה קודמת"):
                st.session_state.current_q_idx -= 1
                st.rerun()
        with col2:
            if q_idx < exam.total_questions - 1:
                if st.button("שאלה הבאה"):
                    # טעינת מנה נוספת במידת הצורך
                    if q_idx + 1 == len(questions):
                        exam.fetch_batch(len(questions))
                    st.session_state.current_q_idx += 1
                    st.rerun()
            else:
                if st.button("סיים בחינה"):
                    st.balloons()
                    st.success("הבחינה הסתיימה בהצלחה!")
