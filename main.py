# Project: מתווך בקליק | Version: B03
# File: main.py
import streamlit as st
from syllabus_data import SYLLABUS
from styles import apply_styles, show_footer
from ai_engine import stream_lesson, fetch_quick_question

# הגדרות דף בסיסיות
st.set_page_config(page_title="מתווך בקליק", layout="wide", page_icon="🏠")
apply_styles("B03")

# --- כותרת ולוגו קבועים (מופיעים בכל הדפים) ---
st.title("🏠 מתווך בקליק")
st.markdown("---")

# אתחול Session State
if "step" not in st.session_state:
    st.session_state.update({
        "user": None,
        "step": "login",
        "selected_topic": None,
        "current_sub": None,
        "lesson_txt": "",
        "quiz_active": False,
        "q_data": None,
        "q_count": 0,
        "show_ans": False
    })

# --- דף כניסה ---
if st.session_state.step == "login":
    st.subheader("ברוכים הבאים למערכת ההכנה למבחן המתווכים 2026")
    u = st.text_input("שם מלא להתחברות:")
    if st.button("כניסה למערכת") and u:
        st.session_state.user = u
        st.session_state.step = "menu"
        st.rerun()

# --- תפריט ראשי ---
elif st.session_state.step == "menu":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים", use_container_width=True):
            st.session_state.step = "study_select"
            st.rerun()
    with c2:
        if st.button("⏱️ מבחן מלא (הכנה)", use_container_width=True):
            st.session_state.step = "exam_mode"
            st.rerun()

# --- בחירת נושא לימוד ---
elif st.session_state.step == "study_select":
    st.subheader("בחר נושא מהסילבוס הרשמי:")
    sel = st.selectbox("נושא מרכזי:", ["בחר נושא..."] + list(SYLLABUS.keys()))
    if sel != "בחר נושא..." and st.button("טען נושא"):
        st.session_state.selected_topic = sel
        st.session_state.step = "lesson_view"
        st.rerun()
    if st.button("🔙 חזרה לתפריט"):
        st.session_state.step = "menu"
        st.rerun()

# --- דף שיעור ושאלות בזק ---
elif st.session_state.step == "lesson_view":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    
    # תצוגת תתי-נושאים בכפתורים
    subs = SYLLABUS.get(topic, [])
    cols = st.columns(len(subs) if len(subs) > 0 else 1)
    for i, s in enumerate(subs):
        if cols[i % len(cols)].button(s, key=f"sub_{i}"):
            st.session_state.update({
                "current_sub": s,
                "lesson_txt": "LOADING",
                "quiz_active": False,
                "q_data": None,
                "q_count": 0,
                "show_ans": False
            })
            st.rerun()

    # הזרמת תוכן ה-AI
    if st.session_state.lesson_txt == "LOADING":
        st.divider()
        st.subheader(st.session_state.current_sub)
        response = stream_lesson(topic, st.session_state.current_sub)
        
        if response:
            full_txt = ""
            placeholder = st.empty()
            try:
                for chunk in response:
                    if chunk.text:
                        full_txt += chunk.text
                        placeholder.markdown(full_txt + "▌")
                placeholder.markdown(full_txt)
                st.session_state.lesson_txt = full_txt
            except Exception as e:
                st.error(f"הזרמת התוכן נפסקה: {e}")
        else:
            st.error("לא ניתן היה לקבל מענה מה-AI. וודא שהמפתח תקין ושיש מכסה פנויה.")

    elif st.session_state.lesson_txt:
        st.divider()
        st.subheader(st.session_state.current_sub)
        st.markdown(st.session_state.lesson_txt)

    # כפתורי פעולה בתחתית
    st.write("")
    f1, f2, f3 = st.columns(3)
    with f1:
        if st.button("🏠 תפריט ראשי"):
            st.session_state.step = "menu"
            st.rerun()
    with f2:
        if st.session_state.lesson_txt and st.session_state.lesson_txt != "LOADING":
            if st.button("📝 שאלת בדיקת הבנה"):
                with st.spinner("מייצר שאלה..."):
                    st.session_state.q_data = fetch_quick_question(topic, st.session_state.current_sub)
                    st.session_state.quiz_active = True
                    st.rerun()

    # הצגת שאלה (אם הופעלה)
    if st.session_state.quiz_active and st.session_state.q_data:
        st.info(f"**שאלה:** {st.session_state.q_data['q']}")
        # לוגיקה לשאלון...
        
show_footer("B03")
