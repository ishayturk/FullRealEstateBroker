import streamlit as st
from logic import initialize_exam

# הגדרות עמוד ו-RTL
st.set_page_config(page_title="סימולטור רשם המתווכים", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="css"] {
        direction: RTL;
        text-align: right;
        font-family: 'Assistant', sans-serif;
    }
    .stButton button { width: 100%; }
    .question-text { font-size: 1.1rem !important; font-weight: 700; margin-bottom: 20px; }
    .sidebar-content { padding: 10px; border-radius: 5px; background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- פונקציית ייצור שאלה ברקע ---
def generate_and_store_next():
    # פונקציה זו תופעל ברקע כדי להכין את השאלה הבאה
    # כאן יבוא הקוד שפונה ל-AI עם ה-get_ethics_prompt
    pass

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.title("מבחן תרגול: אתיקה ודיני תיווך")
    st.write("ברוכים הבאים לסימולציה. המבחן כולל 5 שאלות בנושאי אתיקה וחוק המתווכים.")
    st.write("**משך המבחן:** 5 דקות.")
    
    if st.button("התחל בחינה"):
        state['current_index'] = 0
        state['start_time'] = time.time()
        # ייצור השאלה הראשונה קורה כאן או קרה כבר ברקע
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # חישוב זמן
    elapsed = time.time() - state['start_time']
    remaining = max(0, 300 - int(elapsed))
    
    # Sidebar (בנייד יופיע כדף צף/תפריט)
    with st.sidebar:
        st.header(f"זמן נותר: {remaining // 60}:{remaining % 60:02d}")
        st.progress((state['current_index'] + 1) / 5)
        st.write(f"שאלה {state['current_index'] + 1} מתוך 5")
        
        if st.button("סיים מבחן כעת"):
            state['is_finished'] = True
            st.rerun()

    # תצוגת שאלה
    # כאן נשלפת השאלה מהרשימה שנוצרה דינמית
    # (לצורך הקוד, נניח שיש לנו אובייקט current_q)
    
    st.markdown(f"<div class='question-text'>שאלה {state['current_index']+1}</div>", unsafe_allow_html=True)
    # הצגת טקסט השאלה והאפשרויות...
    
    # כפתורי ניווט
    col1, col2 = st.columns(2)
    with col1:
        if state['current_index'] > 0:
            if st.button("הקודם"):
                state['current_index'] -= 1
                st.rerun()
    with col2:
        # כפתור "הבא" מייצר ברקע את השאלה הבאה אם היא לא קיימת
        button_label = "סיים מבחן" if state['current_index'] == 4 else "השאלה הבאה"
        if st.button(button_label):
            if state['current_index'] < 4:
                state['current_index'] += 1
                # כאן מופעל ה-Pre-fetch לשאלה הבאה
                st.rerun()
            else:
                state['is_finished'] = True
                st.rerun()

# --- עמוד סיכום ומשוב ---
else:
    st.title("תוצאות המבחן")
    # הצגת ציון ומשוב (V ליד תשובה נכונה)
    if st.button("מבחן חדש (איפוס)"):
        st.session_state.clear()
        st.rerun()
