# ==========================================
# Project: מתווך בקליק | Version: 1228-G2
# ==========================================
import streamlit as st
import google.generativeai as genai
import json, re, time, random

st.set_page_config(page_title="מתווך בקליק", layout="wide")

st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    .timer-box {
        position: fixed; top: 10px; left: 10px; background: #ff4b4b; color: white;
        padding: 8px; border-radius: 8px; z-index: 1000; font-weight: bold;
    }
    .nav-overlay {
        background-color: #f0f2f6; padding: 15px; border-radius: 15px;
        border: 1px solid #d1d5db; margin: 10px 0;
    }
    .v-footer { text-align: center; color: rgba(255, 255, 255, 0.1); font-size: 0.7em; }
</style>
""", unsafe_allow_html=True)

# כותרת קבועה לכל האפליקציה
st.title("🏠 מתווך בקליק")

# --- אתחול State ---
if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "used_exams": [], 
        "current_exam_id": None, "exam_qs": [], "current_q_idx": 0, 
        "max_reached_idx": 0, "exam_answers": {}, "start_time": None,
        "show_nav": False, "lesson_txt": ""
    })

# --- לוגיקה לפי שלבים ---

if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.update({"user": u, "step": "menu"}); st.rerun()

elif st.session_state.step == "menu":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים"): st.session_state.step = "study"; st.rerun()
    with c2:
        if st.button("⏱️ גש למבחן מלא"): st.session_state.step = "exam_prep"; st.rerun()

# ... (שאר חלקי הקוד: study, exam_prep, exam_run, results נשארים ללא שינוי)
