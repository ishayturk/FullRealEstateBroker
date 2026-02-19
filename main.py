import streamlit as st
import json
import os

# הגדרות עמוד
st.set_page_config(page_title="מבחן רשם המתווכים", layout="wide", initial_sidebar_state="collapsed")

def load_exam(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # אתחול מצבים
    if 'page' not in st.session_state:
        st.session_state.page = 'explanation'
        st.session_state.current_q_idx = 0
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    # --- עמוד הסבר ---
    if st.session_state.page == 'explanation':
        st.title("🎓 הוראות לבחינה")
        st.write("קרא את ההוראות בעיון. לאחר שתלחץ על התחל, לא תוכל לדלג על שאלות.")
        
        exam_files = [f for f in os.listdir('.') if f.endswith('.json')]
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
        
        # עדכון Sidebar - מספרי שאלות לא פעילים
        st.sidebar.title("רשימת שאלות")
        for i in range(len(questions)):
            status = "✅" if i in st.session_state.user_answers else "⚪"
            if i == curr_idx:
                st.sidebar.markdown(f"**📍 שאלה {i+1}**")
            else:
                st.sidebar.text(f"{status} שאלה {i+1}")

        # הצגת השאלה הנוכחית
        if not st.session_state.submitted:
            q = questions[curr_idx]
            st.header(f"שאלה {curr_idx + 1} מתוך {len(questions)}")
            st.subheader(q['question'])
            
            # בחירת תשובה
            choice = st.radio("בחר תשובה:", q['options'], key=f"q_{curr_idx}", index=None)
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("לשאלה הבאה"):
                    if choice:
                        st.session_state.user_answers[curr_idx] = choice
                        if curr_idx < len(questions) - 1:
                            st.session_state.current_q_idx += 1
                            st.rerun()
                        else:
                            st.warning("זו השאלה האחרונה. ניתן להגיש את המבחן.")
                    else:
                        st.error("חובה לבחור תשובה כדי להתקדם.")
            
            with col2:
                if curr_idx == len(questions) - 1 and len(st.session_state.user_answers) == len(questions):
                    if st.button("הגש מבחן"):
                        st.session_state.submitted = True
                        st.rerun()

        # --- עמוד תוצאות (רק אחרי הגשה) ---
        else:
            st.title("תוצאות המבחן")
            correct_count = 0
            for i, q in enumerate(questions):
                user_ans = st.session_state.user_answers.get(i)
                is_correct = user_ans == q['answer']
                if is_correct: correct_count += 1
                
                with st.expander(f"שאלה {i+1}: {'✅' if is_correct else '❌'}"):
                    st.write(q['question'])
                    st.write(f"התשובה שלך: {user_ans}")
                    st.write(f"התשובה הנכונה: {q['answer']}")
            
            score = (correct_count / len(questions)) * 100
            st.metric("ציון סופי", f"{score:.0f}")
            if st.button("חזרה לתפריט ראשי"):
                for key in list(st.session_state.keys()): del st.session_state[key]
                st.rerun()

if __name__ == "__main__":
    main()
