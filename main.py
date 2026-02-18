# main.py | Version: C-01
import streamlit as st
from app_data import TOPICS_DATA
from ai_logic import stream_ai_lesson
from ui_utils import apply_design, navigation_footer

# הגדרת הגדרות דף בסיסיות
st.set_page_config(page_title="מתווך בקליק", layout="centered")

# אתחול ה-Session State (ניהול מצבי הדפים)
if "step" not in st.session_state:
    st.session_state.update({
        "user": None,
        "step": "login",
        "lesson_txt": "",
        "current_sub": None
    })

apply_design()

# --- דף כניסה ---
if st.session_state.step == "login":
    st.title("🏠 מתווך בקליק")
    st.subheader("הכנה למבחן המתווכים")
    user_input = st.text_input("הכנס שם מלא כדי להתחיל:")
    if st.button("כניסה למערכת") and user_input:
        st.session_state.user = user_input
        st.session_state.step = "menu"
        st.rerun()

# --- תפריט ראשי ---
elif st.session_state.step == "menu":
    st.header(f"שלום, {st.session_state.user}")
    st.write("מה תרצה לעשות היום?")
    if st.button("📚 לימוד נושאים ממוקד"):
        st.session_state.step = "study"
        st.rerun()
    
    # כאן יתווסף בעתיד כפתור המבחן הגדול

# --- בחירת נושא לימוד ---
elif st.session_state.step == "study":
    st.subheader("בחר נושא לימוד")
    selected_main = st.selectbox("בחר נושא ראשי:", ["בחר נושא"] + list(TOPICS_DATA.keys()))
    
    if selected_main != "בחר נושא":
        st.write(f"תתי-נושאים ב{selected_main}:")
        for sub in TOPICS_DATA[selected_main]:
            if st.button(sub, key=f"btn_{sub}"):
                st.session_state.current_sub = sub
                st.session_state.step = "lesson_run"
                st.session_state.lesson_txt = "LOADING"
                st.rerun()
    navigation_footer()

# --- הרצת שיעור AI ---
elif st.session_state.step == "lesson_run":
    st.subheader(f"📖 שיעור: {st.session_state.current_sub}")
    
    if st.session_state.lesson_txt == "LOADING":
        full_text = ""
        placeholder = st.empty()
        # קריאה למנוע ה-AI מהקובץ הנפרד
        response = stream_ai_lesson(st.session_state.current_sub)
        
        if response:
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
            st.session_state.lesson_txt = full_text
    else:
        st.markdown(st.session_state.lesson_txt)
    
    navigation_footer()
