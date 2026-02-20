import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_question_to_queue

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right !important; }
    [data-testid="stSidebar"] { direction: rtl !important; }
    
    /* רדיו: עיגול מימין ומרווח של 25 פיקסלים */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 25px !important;
        display: flex !important;
    }
    
    /* הנמכת השעון למניעת חיתוך וייצוב המסגרת */
    iframe { 
        margin-top: 35px !important; 
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    if not state['questions']: fetch_question_to_queue()
    st.title("הסבר לבחינת רישיון למתווכים")
    st.markdown("""
    • לבחינה 25 שאלות  
    • זמן הבחינה: 90 דקות  
    • מעבר לשאלה הבאה מתאפשר רק לאחר סימון תשובה  
    • ניווט בסידבר מתאפשר רק לשאלות שכבר ענית עליהן והמשכת הלאה
    """)
    agreed = st.checkbox("קראתי ומאשר את תנאי הבחינה")
    if st.button("התחל בחינה", disabled=not agreed):
        state['start_time'] = time.time()
        state['current_index'] = 0
        fetch_question_to_queue()
        st.rerun()

# --- עמוד בחינה ---
elif not state['is_finished']:
    remaining = max(0, 5400 - int(time.time() - state['start_time']))
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # שעון HTML יציב עם רקע לבן זהה לדף
    timer_html = f"""
    <div style="background-color: #ffffff; padding: 15px; text-align: center; overflow: hidden;">
        <span id="c" style="font-family: monospace; font-size: 40px; font-weight: bold; color: #1e1e1e;">00:00</span>
    </div>
    <script>
        var sec = {remaining};
        function t() {{
            var m = Math.floor(sec/60), s = sec%60;
            document.getElementById('c').innerHTML = (m<10?'0':'')+m+":"+(s<10?'0':'')+s;
            if (sec>0) {{ sec--; setTimeout(t, 1000); }}
            else {{ window.parent.location.reload(); }}
        }}
        t();
    </script>
    """
    components.html(timer_html, height=100)

    with st.sidebar:
        st.write("### ניווט לשאלות עבר")
        for i in range(25):
            # כפתור פעיל רק לשאלות עבר (שכבר עברת אותן)
            is_past = i < state['current_index']
            if st.button(f"שאלה {i+1}", key=f"n_{i}", disabled=not is_past):
                state['current_index'] = i
                st.rerun()

    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.write(q['question_text'])
        
        ans = state['answers'].get(state['current_index'], None)
        choice = st.radio("", q['options'], index=ans, key=f"r_{state['current_index']}", label_visibility="collapsed")
        
        if choice is not None:
            state['answers'][state['current_index']] = q['options'].index(choice)

        st.divider()
        col1, col2 = st.columns(2)
        with col2:
            if state['current_index'] > 0:
                if st.button("שאלה קודמת ➡️"):
                    state['current_index'] -= 1
                    st.rerun()
        with col1:
            if state['current_index'] < 24:
                can_next = state['current_index'] in state['answers']
                if st.button("⬅️ שאלה הבאה", disabled=not can_next):
                    state['current_index'] += 1
                    if len(state['questions']) <= state['current_index'] + 1:
                        fetch_question_to_queue()
                    st.rerun()
            else:
                if st.button("🏁 סיים בחינה"):
                    state['is_finished'] = True
                    st.rerun()
    st.rerun()

else:
    st.header("הבחינה הסתיימה")
    st.write(f"ענית על {len(state['answers'])} שאלות.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
