import streamlit as st
import time
from logic import initialize_exam, generate_question_sync

# הגדרות דף - סידבר קבוע (לא ניתן לסגירה)
st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="expanded")

# CSS קשיח לפתרון בעיות ויזואליות: RTL, רדיו מימין, שעון וכפתורים שקופים
st.markdown("""
    <style>
    /* יישור RTL גלובלי */
    .stApp, [data-testid="stSidebar"], .stMarkdown, p, h1, h2, h3, label {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* חסימת אפשרות סגירת הסידבר */
    [data-testid="sidebar-close"] { display: none !important; }
    
    /* רדיו באטן - הנקודה מימין למלל (RTL קשיח) */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        display: flex !important;
        padding: 8px 0;
    }

    /* עיצוב שעון שקט במרכז */
    .timer-box {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        color: #333;
        background-color: #f8f9fa;
        padding: 10px 20px;
        border-radius: 12px;
        border: 1px solid #ccc;
        margin: 10px auto;
        width: fit-content;
    }

    /* כפתורים שקופים ללא צבע אדום */
    .stButton>button {
        width: 100%;
        background-color: transparent !important;
        color: #444 !important;
        border: 1px solid #444 !important;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #eeeeee !important;
        border-color: #000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# אתחול ה-State מקובץ הלוגיקה
initialize_exam()
state = st.session_state.exam_state

# --- עמוד הסבר לבחינה ---
if state['current_index'] == -1:
    st.title("הסבר לבחינת רישיון למתווכים")
    
    st.markdown("""
    * לבחינה 25 שאלות אמריקאיות
    * זמן הבחינה הוא 90 דקות
    * ניתן לעבור לשאלה הבאה רק לאחר סימון תשובה על השאלה הנוכחית
    * ניתן לנווט בין השאלות שכבר ענית עליהן
    * סיימת את הבחינה לחץ/י על כפתור סיים בחינה
    * בתום הזמן המבחן מסתיים במיידי ולא תוכל להמשיך לנווט ולענות על שאלות
    * בסיום הבחינה יזום או בשל הזמן תקבל משוב על הבחינה
    """)
    
    st.divider()
    agreed = st.checkbox("קראתי ומאשר")
    
    if st.button("התחל בחינה", disabled=not agreed):
        state['questions'] = [generate_question_sync(0)]
        state['current_index'] = 0
        state['start_time'] = time.time()
        st.rerun()

# --- עמוד בחינה פעיל ---
elif not state['is_finished']:
    total_time = 5400 # 90 דקות
    elapsed = time.time() - state['start_time']
    remaining = max(0, total_time - int(elapsed))
    
    if remaining <= 0:
        state['is_finished'] = True
        st.rerun()

    # שעון מרכזי
    st.markdown(f"<div class='timer-box'>⏳ {int(remaining // 60):02d}:{int(remaining % 60):02d}</div>", unsafe_allow_html=True)

    # סידבר עם גריד של 4 שאלות בשורה
    with st.sidebar:
        st.write("### ניווט שאלות")
        for row in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                idx = row + i
                if idx < 25:
                    can_nav = idx < len(state['questions'])
                    if cols[i].button(f"{idx+1}", key=f"nav_{idx}", disabled=not can_nav):
                        state['current_index'] = idx
                        st.rerun()

    # הצגת השאלה מהזיכרון
    q = state['questions'][state['current_index']]
    st.subheader(f"שאלה {state['current_index'] + 1}")
    st.markdown(f"#### {q['question_text']}")
    
    ans = state['answers'].get(state['current_index'], None)
    choice = st.radio("", q['options'], index=ans, key=f"q_{state['current_index']}", label_visibility="collapsed")
    
    if choice is not None:
        state['answers'][state['current_index']] = q['options'].index(choice)

    st.divider()
    
    col_next, col_finish, col_prev = st.columns([1, 1, 1])
    
    with col_prev:
        if state['current_index'] > 0:
            if st.button("שאלה קודמת ➡️"):
                state['current_index'] -= 1
                st.rerun()
                
    with col_finish:
        if state['current_index'] == 24 or len(state['answers']) >= 25:
            if st.button("🏁 סיים בחינה"):
                state['is_finished'] = True
                st.rerun()

    with col_next:
        if state['current_index'] < 24:
            has_answered = state['current_index'] in state['answers']
            if st.button("⬅️ שאלה הבאה", disabled=not has_answered):
                state['current_index'] += 1
                if len(state['questions']) <= state['current_index']:
                    state['questions'].append(generate_question_sync(state['current_index']))
                st.rerun()

    time.sleep(1)
    st.rerun()

# --- עמוד סיום ---
else:
    st.header("הבחינה הסתיימה")
    st.subheader(f"ענית על {len(state['answers'])} שאלות מתוך 25.")
    if st.button("חזרה להתחלה"):
        st.session_state.clear()
        st.rerun()
