import streamlit as st
import time
import streamlit.components.v1 as components
from logic import initialize_exam, fetch_question_to_queue

st.set_page_config(page_title="סימולטור רשם המתווכים", layout="wide")

# CSS לתיקון יישור לימין (RTL) וסידור הרדיו
st.markdown("""
    <style>
    /* יישור גורף לימין לכל האפליקציה */
    .stApp, [data-testid="stSidebar"], [data-testid="stMarkdownContainer"], .stRadio {
        direction: rtl !important;
        text-align: right !important;
    }

    /* הצמדת כותרות וטקסט לימין */
    h1, h2, h3, .stSubheader, p, li {
        text-align: right !important;
        direction: rtl !important;
    }

    /* תיקון רדיו: עיגול הבחירה מימין למלל עם מרווח */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 20px !important;
        display: flex !important;
    }

    /* מרווח עליון כדי למנוע חפיפה עם התפריט */
    .block-container { padding-top: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר ---
if state['current_index'] == -1:
    if not state['questions']: fetch_question_to_queue()
    st.title("בחינת רישיון למתווכים במקרקעין")
    st.markdown("""
    ### הוראות לבחינה:
    1. המבחן כולל **25 שאלות** בפורמט אמריקאי.
    2. לרשותך **90 דקות** לסיום המבחן.
    3. לא ניתן לעבור לשאלה הבאה ללא סימון תשובה.
    4. הניווט בסידבר יתאפשר **רק לשאלות עבר** שכבר ענית עליהן.
    """)
    
    agreed = st.checkbox("אני מאשר/ת את תנאי הבחינה ומוכן/ה להתחיל")
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

    # השעון כפי שהיה בגרסה היציבה שלך (ללא שינוי מבנה)
    timer_html = f"""
    <div style="text-align: center; background: #ffffff; padding: 10px;">
        <span id="t" style="font-family: monospace; font-size: 35px; font-weight: bold;">00:00</span>
    </div>
    <script>
        var s = {remaining};
        function update() {{
            var m = Math.floor(s/60), sec = s%60;
            document.getElementById('t').innerHTML = (m<10?'0':'')+m+":"+(sec<10?'0':'')+sec;
            if (s > 0) {{ s--; setTimeout(update, 1000); }}
            else {{ window.parent.location.reload(); }}
        }}
        update();
    </script>
    """
    components.html(timer_html, height=70)

    # סידבר עם לוגיקת ניווט עבר בלבד
    with st.sidebar:
        st.write("### ניווט (שאלות עבר)")
        for i in range(25):
            # כפתור פעיל רק אם זו שאלת עבר (i קטן מהאינדקס הנוכחי)
            is_past = i < state['current_index']
            if st.button(f"שאלה {i+1}", key=f"nav_{i}", disabled=not is_past):
                state['current_index'] = i
                st.rerun()

    # הצגת השאלה
    if state['current_index'] < len(state['questions']):
        q = state['questions'][state['current_index']]
        st.subheader(f"שאלה {state['current_index'] + 1}")
        st.write(q['question_text'])
        
        current_ans = state['answers'].get(state['current_index'], None)
        choice = st.radio("", q['options'], index=current_ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
        
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
                answered = state['current_index'] in state['answers']
                if st.button("⬅️ שאלה הבאה", disabled=not answered):
                    state['current_index'] += 1
                    if len(state['questions']) <= state['current_index']:
                        fetch_question_to_queue()
                    st.rerun()
            else:
                if st.button("🏁 סיים בחינה"):
                    state['is_finished'] = True
                    st.rerun()
    
    time.sleep(1)
    st.rerun()

else:
    st.title("הבחינה הסתיימה")
    st.write(f"השלמת {len(state['answers'])} שאלות מתוך 25.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
