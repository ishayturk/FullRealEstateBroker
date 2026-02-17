# Project: מתווך בקליק | Version: B02
# File: main.py
import streamlit as st
from syllabus_data import SYLLABUS
from styles import apply_styles, show_footer
from ai_engine import stream_lesson, fetch_quick_question

# הגדרות דף בסיסיות
st.set_page_config(page_title="מתווך בקליק - B02", layout="wide")
apply_styles("B02")

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
        "correct_answers": 0,
        "show_ans": False
    })

# --- דף כניסה ---
if st.session_state.step == "login":
    st.title("🏠 מתווך בקליק")
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.user = u
        st.session_state.step = "menu"
        st.rerun()

# --- תפריט ראשי ---
elif st.session_state.step == "menu":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים"):
            st.session_state.step = "study_select"
            st.rerun()
    with c2:
        if st.button("⏱️ מבחן מלא (מהמאגר)"):
            st.session_state.step = "exam_mode"
            st.rerun()

# --- בחירת נושא לימוד ---
elif st.session_state.step == "study_select":
    st.subheader("בחר נושא ללימוד:")
    sel = st.selectbox("נושא מרכזי:", ["בחר..."] + list(SYLLABUS.keys()))
    if sel != "בחר..." and st.button("טען נושא"):
        st.session_state.selected_topic = sel
        st.session_state.step = "lesson_view"
        st.rerun()
    if st.button("חזרה לתפריט"):
        st.session_state.step = "menu"
        st.rerun()

# --- דף שיעור ושאלות בזק ---
elif st.session_state.step == "lesson_view":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    
    subs = SYLLABUS.get(topic, [])
    cols = st.columns(len(subs))
    for i, s in enumerate(subs):
        if cols[i].button(s, key=f"sub_{i}"):
            st.session_state.update({
                "current_sub": s,
                "lesson_txt": "LOADING",
                "quiz_active": False,
                "q_data": None,
                "q_count": 0,
                "show_ans": False
            })
            st.rerun()

    # הצגת שיעור עם הגנה מפני קריסה
    if st.session_state.lesson_txt == "LOADING":
        st.subheader(st.session_state.current_sub)
        response = stream_lesson(topic, st.session_state.current_sub)
        
        if response:
            full_txt = ""
            placeholder = st.empty()
            try:
                for chunk in response:
                    full_txt += chunk.text
                    placeholder.markdown(full_txt + "▌")
                placeholder.markdown(full_txt)
                st.session_state.lesson_txt = full_txt
            except Exception as e:
                st.error("הייתה בעיה בהזרמת התוכן מה-AI. נסה ללחוץ שוב על הנושא.")
                st.session_state.lesson_txt = ""
        else:
            st.error("שגיאה: לא התקבל מענה מה-AI. בדוק את ה-API Key ב-Secrets.")
            st.session_state.lesson_txt = ""

    elif st.session_state.lesson_txt:
        st.subheader(st.session_state.current_sub)
        st.markdown(st.session_state.lesson_txt)

    # שאלון בזק (הבנה)
    if st.session_state.quiz_active and st.session_state.q_data:
        st.markdown("---")
        st.subheader(f"📝 בדיקת הבנה: {st.session_state.current_sub}")
        q = st.session_state.q_data
        ans = st.radio(q['q'], q['options'], index=None, key=f"q_radio_{st.session_state.q_count}")
        
        if st.button("בדיקת תשובה") or st.session_state.show_ans:
            st.session_state.show_ans = True
            if ans == q['correct']: st.success("נכון!")
            else: st.error(f"לא מדויק. התשובה: {q['correct']}")
            st.info(f"הסבר: {q['explain']}")
            if st.button("שאלה הבאה (בזק)"):
                with st.spinner("טוען שאלה..."):
                    st.session_state.q_data = fetch_quick_question(topic, st.session_state.current_sub)
                    st.session_state.q_count += 1
                    st.session_state.show_ans = False
                    st.rerun()

    # כפתורי ניווט תחתונים
    st.write("")
    footer_cols = st.columns([2, 2, 2])
    with footer_cols[0]:
        if st.session_state.lesson_txt and not st.session_state.quiz_active:
            if st.button("📝 שאלות בזק לשיעור זה"):
                with st.spinner("מייצר שאלת בזק..."):
                    st.session_state.q_data = fetch_quick_question(topic, st.session_state.current_sub)
                    if st.session_state.q_data:
                        st.session_state.quiz_active = True
                        st.session_state.q_count = 1
                        st.rerun()
                    else:
                        st.error("לא הצלחתי לייצר שאלה. נסה שוב.")
    with footer_cols[1]:
        if st.button("🏠 תפריט ראשי"):
            st.session_state.step = "menu"
            st.rerun()

# --- מצב מבחן ---
elif st.session_state.step == "exam_mode":
    st.header("⏱️ מערכת המבחנים המלאה")
    st.info("כאן נחבר את המאגר הגדול שלך.")
    if st.button("חזרה לתפריט"):
        st.session_state.step = "menu"
        st.rerun()

show_footer("B02")
