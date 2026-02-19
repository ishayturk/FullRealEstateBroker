import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# CSS קשיח לפתרון ה-RTL והרדיו באטן
st.markdown("""
    <style>
    /* יישור גלובלי לימין */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3 {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* רדיו באטן - הנקודה מימין לטקסט */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        font-size: 1.3rem !important;
        display: flex !important;
    }

    /* צ'קבוקס הסבר - ריבוע מימין למלל */
    [data-testid="stCheckbox"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 30px !important;
    }

    .question-title { font-size: 1.6rem; font-weight: bold; margin-bottom: 20px; }
    
    /* הסתרת רכיבים מיותרים */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    st.header("דף הסבר והוראות לבחינה")
    st.write("מבחן סימולציה באתיקה למתווכים. 5 שאלות, 5 דקות.")
    
    agreed = st.checkbox("קראתי והבנתי את ההוראות לבחינה")
    state['confirmed_instructions'] = agreed

    if st.button("התחל בחינה"):
        if agreed:
            state['questions'] = [generate_question_sync(0)]
            state['current_index'] = 0
            state['start_time'] = time.time()
            st.rerun()
        else:
            st.error("חובה לאשר את ההוראות תחילה.")

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    # שעון JS שקט באמת בסידבר
    with st.sidebar:
        st.write("### ⏳ זמן נותר")
        # הטיימר רץ ב-JS בדפדפן ולא מרענן את ה-Python
        st.markdown("""
            <div id="timer" style="font-size: 30px; font-weight: bold; text-align: center; border: 2px solid #333; border-radius: 10px; padding: 10px;">05:00</div>
            <script>
            var seconds = 300;
            var x = setInterval(function() {
                var mins = Math.floor(seconds / 60);
                var secs = seconds % 60;
                document.getElementById("timer").innerHTML = (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
                seconds--;
                if (seconds < 0) {
                    clearInterval(x);
                    window.parent.postMessage({type: 'streamlit:set_widget_value', data: true, widgetId: 'time_up'}, '*');
                }
            }, 1000);
            </script>
        """, unsafe_allow_html=True)
        
        # מנגנון סיום אוטומטי כשנגמר הזמן
        if st.hidden_input(key="time_up"):
             state['is_finished'] = True
             st.rerun()

        st.divider()
        st.write("### ניווט")
        cols = st.columns(4)
        for i in range(5):
            if cols[i % 4].button(f"{i+1}", key=f"n_{i}", type="primary" if i == state['current_index'] else "secondary"):
                while len(state['questions']) <= i:
                    state['questions'].append(generate_question_sync(len(state['questions'])))
                state['current_index'] = i
                st.rerun()

    # השאלה
    q = state['questions'][state['current_index']]
    st.markdown(f"<div class='question-title'>שאלה {state['current_index'] + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:1.4rem; margin-bottom:20px;'>{q['question_text']}</div>", unsafe_allow_html=True)
    
    ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice is not None:
        state['answers'][state['current_index']] = q['options'].index(choice)

    st.divider()
    
    col_next, col_finish, col_prev = st.columns([1,1,1])
    
    with col_prev:
        if state['current_index'] > 0:
            if st.button("שאלה קודמת ➡️"):
                state['current_index'] -= 1
                st.rerun()
                
    with col_finish:
        # כפתור הגש מופיע רק בשאלה האחרונה
        if state['current_index'] == 4:
            if st.button("🏁 סיים והגש בחינה", type="primary"):
                state['is_finished'] = True
                st.rerun()

    with col_next:
        if state['current_index'] < 4:
            has_ans = state['current_index'] in state['answers']
            if st.button("⬅️ שאלה הבאה", disabled=not has_ans):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

# --- עמוד סיום נקי ---
else:
    st.header("הבחינה הסתיימה")
    st.divider()
    # הצגת כמות תשובות בלבד כפי שביקשת (ללא ציון)
    st.subheader(f"ענית על {len(state['answers'])} שאלות מתוך 5.")
    st.write("תודה על השתתפותך בסימולציה.")
    
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
