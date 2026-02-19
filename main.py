import streamlit as st
import json
import os

# הגדרות עמוד ויישור לימין באמצעות CSS
st.set_page_config(page_title="מבחן רשם המתווכים", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    div[role="radiogroup"] {
        direction: RTL;
        text-align: right;
    }
    div.stButton > button {
        width: 100%;
    }
    /* יישור ה-Sidebar */
    [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

def load_exam(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'explanation'
        st.session_state.current_q_idx = 0
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    # --- עמוד הסבר ---
    if st.session_state.page == 'explanation':
        st.title("🎓 הוראות לבחינה")
        st.write("ברוכים הבאים למערכת התרגול. קראו את ההוראות בעיון:")
        st.info("""
        * המעבר בין השאלות הוא ליניארי בלבד.
        * לא ניתן לדלג על שאלה מבלי לענות עליה.
        * לאחר לחיצה על 'לשאלה הבאה', השאלה תסומן בביצוע בתפריט הצד.
        * התוצאות והתשובות הנכונות יוצגו רק בסוף הבחינה.
        """)
        
        exam_files = [f for f in os.listdir('.') if f.endswith('.json')]
        if not exam_files:
            st.warning("מכין קבצי בחינה... אנא המתן שניה ורענן.")
            return

        selected_file = st.selectbox("בחר מועד בחינה:", exam_files)
        
        if st.button("התחל בחינה"):
            st.session_state.exam_data = load_exam(selected_file)
            st.session_state.page = 'exam'
            st.rerun()

    # --- עמוד הבחינה ---
    elif st.session_state.page == 'exam':
        exam = st.session_state.exam_data
        questions = exam['questions']
        curr_idx = st.session_state.current_q_idx
        
        # Sidebar - מפת התקדמות (לא פעילה ללחיצה)
        st.sidebar.title("מפת שאלות")
        for i in range(len(questions)):
            if i < curr_idx:
                status = "✅" # ענה כבר
            elif i == curr_idx:
                status = "📍" # נוכחי
            else:
                status = "⚪" # טרם הגיע
            st.sidebar.text(f"{status} שאלה {i+1}")

        if not st.session_state.submitted:
            q = questions[curr_idx]
            st.header(f"שאלה {curr_idx + 1} מתוך {len(questions)}")
            st.markdown(f"### {q['question']}")
            
            # רדיו לבחירת תשובה
            choice = st.radio("בחר את התשובה הנכונה:", q['options'], key=f"q_{curr_idx}", index=None)
            
            st.divider()
            
            # כפתור התקדמות
            if curr_idx < len(questions) - 1:
                if st.button("שמור ולשאלה הבאה ⬅️"):
                    if choice:
                        st.session_state.user_answers[curr_idx] = choice
                        st.session_state.current_q_idx += 1
                        st.rerun()
                    else:
                        st.error("חובה לענות על השאלה לפני שעוברים הלאה.")
            else:
                # שאלה אחרונה
                if st.button("סיים והגש בחינה 🏁"):
                    if choice:
                        st.session_state.user_answers[curr_idx] = choice
                        st.session_state.submitted = True
                        st.rerun()
                    else:
                        st.error("חובה לענות על השאלה האחרונה לפני ההגשה.")

        # --- עמוד תוצאות ---
        else:
            st.title("סיכום ותוצאות")
            correct_count = sum(1 for i, q in enumerate(questions) if st.session_state.user_answers.get(i) == q['answer'])
            score = (correct_count / len(questions)) * 100
            
            st.metric("ציון סופי", f"{score:.0f}")
            
            for i, q in enumerate(questions):
                user_ans = st.session_state.user_answers.get(i)
                is_correct = user_ans == q['answer']
                with st.expander(f"שאלה {i+1}: {'✅' if is_correct else '❌'}"):
                    st.write(f"**השאלה:** {q['question']}")
                    st.write(f"**תשובתך:** {user_ans}")
                    st.write(f"**תשובה נכונה:** {q['answer']}")

            if st.button("חזרה לתפריט ראשי"):
                for key in list(st.session_state.keys()): del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    main()
