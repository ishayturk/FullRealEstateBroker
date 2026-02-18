# Version: C-01 (Clean UI)
import streamlit as st
import time

def render_rtl():
    """הזרקת CSS ליישור לימין"""
    st.markdown("""<style>
        .stApp, div[role="radiogroup"], section[data-testid="stSidebar"] > div { direction: rtl; text-align: right; }
        p, span, h1, h2, h3, h4, label { text-align: right; direction: rtl; }
    </style>""", unsafe_allow_html=True)

def show_results(user_answers, exam_data):
    """הצגת תוצאות פשוטה"""
    score = 0
    for i, q in enumerate(exam_data):
        ans = user_answers.get(i, "")
        correct = str(q['תשובה_נכונה']).strip()
        if str(ans).strip() == correct:
            score += 1
    st.metric("ציון סופי", f"{int((score/25)*100)}/100")
