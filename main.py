import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_question_to_queue

st.set_page_config(page_title="סימולטור בחינה", layout="wide")

# CSS ממוקד: יישור רדיו לימין מבלי להרוס את הצ'קבוקס או הסידבר
st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right !important; }
    [data-testid="stSidebar"] { direction: rtl !important; }
    
    /* עיגול הרדיו לימין המלל */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        display: flex !important;
    }

    /* החזרת הצ'קבוקס למבנה רגיל (מלל מימין לצ'ק) */
    [data-testid="stCheckbox"] label {
        flex-direction: row !important;
    }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- דף הסבר ---
if state['current_index'] == -1:
    if not state['questions']: fetch_question_to_queue()
    st.title("הוראות לבחינה")
    st.markdown("""
    * המבחן כולל 25 שאלות אמריקאיות.
    * משך הבחינה: 90 דקות.
    * מעבר לשאלה הבאה מותנה בסימון תשובה.
    * ניתן לנווט אחורה רק לשאלות שכבר ענית עליהן.
    """)
    
    agreed = st.checkbox("אני מאשר את תנאי הבחינה")
    if st.button("התחל בחינה", disabled=not agreed):
        state['start_time'] = time.time()
        state['current_index'] = 0
        fetch_question_to_queue()
        st.rerun()

# --- עמוד בחינה ---
elif not state['is_finished']:
    elapsed = int(time.time() - state['start_time'])
    remaining = max(0, 5400 - elapsed)
    
    # שעון נקי בתוך iframe
    timer_html = f"""
    <div style="text-align: center; font-family: monospace; font-size: 35px; font-weight: bold;">
        <span id="t">00:00</span>
    </div>
    <script>
        var s = {remaining};
        function update() {{
            var m = Math.floor(s/60), sec = s%60;
            document.getElementById('t').innerHTML = (m<10?'0':'')+m+":"+(sec<10?'0':'')+sec;
            if (s > 0) {{ s--; setTimeout(update, 1000); }}
        }}
        update();
    </script>
    """
    components.html(timer_html, height=60)

    with st.sidebar:
        st.write("### ניווט")
        for i in range(25):
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
        c1, c2 = st.columns(2)
        with c2:
            if state['current_index'] > 0:
                if st.button("שאלה קודמת"):
                    state['current_index'] -= 1
                    st.rerun()
        with c1:
            if state['current_index'] < 24:
                can_next = state['current_index'] in state['answers']
                if st.button("שאלה הבאה", disabled=not can_next):
                    state['current_index'] += 1
                    fetch_question_to_queue()
                    st.rerun()
            else:
                if st.button("סיים בחינה"):
                    state['is_finished'] = True
                    st.rerun()
    else:
        st.info("טוען שאלה...")
        time.sleep(1)
        st.rerun()

else:
    st.header("סיום המבחן")
    st.write(f"השלמת {len(state['answers'])} שאלות.")
    if st.button("התחלה מחדש"):
        st.session_state.clear()
        st.rerun()
