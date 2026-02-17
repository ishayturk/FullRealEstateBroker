# ==========================================
# Project: מתווך בקליק | Version: 1225-G2 (Test Mode)
# ==========================================
import streamlit as st
import time, random

st.set_page_config(page_title="מתווך בקליק", layout="wide")

st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .timer-box {
        position: fixed; top: 10px; left: 10px; background: #ff4b4b; color: white;
        padding: 8px; border-radius: 8px; z-index: 1000; font-size: 0.9em;
    }
    .nav-overlay {
        background-color: #f0f2f6; padding: 15px; border-radius: 15px;
        border: 1px solid #d1d5db; margin-bottom: 20px;
    }
    .v-footer { text-align: center; color: rgba(255, 255, 255, 0.1); font-size: 0.7em; }
</style>
""", unsafe_allow_html=True)

# מאגר לבדיקה מהירה
EXAMS_DATABASE = {
    "test_exam": {
        "name": "מבחן בדיקה מהיר (3 דקות)",
        "questions": [
            {"q": f"שאלה לבדיקה מספר {i+1}", "options": ["תשובה א", "תשובה ב", "תשובה ג", "תשובה ד"], "correct_idx": 0}
            for i in range(25)
        ]
    }
}

if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "used_exams": [], 
        "current_exam_id": None, "exam_qs": [], 
        "current_q_idx": 0, "max_reached_idx": 0,
        "exam_answers": {}, "start_time": None, "show_nav": False
    })

if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.update({"user": u, "step": "menu"}); st.rerun()

elif st.session_state.step == "menu":
    st.title("🏠 מתווך בקליק - מצב בדיקה")
    if st.button("⏱️ התחל מבחן בדיקה (3 דקות)"):
        st.session_state.update({
            "current_exam_id": "test_exam", "step": "exam_run", "start_time": time.time(),
            "exam_qs": EXAMS_DATABASE["test_exam"]["questions"][:5],
            "exam_answers": {}, "current_q_idx": 0, "max_reached_idx": 0
        })
        st.rerun()

elif st.session_state.step == "exam_run":
    # טיימר - הוגדר ל-180 שניות (3 דקות)
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 180 - int(elapsed)) 
    
    if rem <= 0:
        st.session_state.step = "time_up"; st.rerun()
    
    mins, secs = divmod(rem, 60)
    st.markdown(f'<div class="timer-box">⏳ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    # לוח ניווט
    if st.button("📱 לוח ניווט"): st.session_state.show_nav = not st.session_state.show_nav
    if st.session_state.show_nav:
        st.markdown('<div class="nav-overlay">', unsafe_allow_html=True)
        cols = st.columns(5)
        for i in range(25):
            with cols[i%5]:
                if i > st.session_state.max_reached_idx:
                    st.button(f"🔒 {i+1}", key=f"n_{i}", disabled=True)
                else:
                    label = f"{i+1} {'✅' if i in st.session_state.exam_answers else ''}"
                    if st.button(label, key=f"n_{i}"):
                        st.session_state.current_q_idx = i; st.session_state.show_nav = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # הצגת שאלה
    idx = st.session_state.current_q_idx
    q = st.session_state.exam_qs[idx]
    st.subheader(f"שאלה {idx + 1}")
    ans = st.radio(q['q'], q['options'], key=f"q_{idx}", index=None if idx not in st.session_state.exam_answers else q['options'].index(st.session_state.exam_answers[idx]))
    if ans: st.session_state.exam_answers[idx] = ans

    c1, c2, c3 = st.columns(3)
    with c1:
        if idx > 0:
            if st.button("⬅️ הקודם"): st.session_state.current_q_idx -= 1; st.rerun()
    with c2:
        if st.button("🏠 תפריט"): st.session_state.step = "menu"; st.rerun()
    with c3:
        if idx < 24:
            if st.button("הבא ➡️"):
                if idx == st.session_state.max_reached_idx: st.session_state.max_reached_idx += 1
                if idx == len(st.session_state.exam_qs) - 1 and len(st.session_state.exam_qs) < 25:
                    st.session_state.exam_qs += EXAMS_DATABASE["test_exam"]["questions"][len(st.session_state.exam_qs):len(st.session_state.exam_qs)+5]
                st.session_state.current_q_idx += 1; st.rerun()
        else:
            if st.button("🏁 הגש מבחן"): st.session_state.step = "results"; st.rerun()

elif st.session_state.step == "time_up":
    st.error("⌛ נגמר הזמן!")
    if st.button("צפה בתוצאות"): st.session_state.step = "results"; st.rerun()

elif st.session_state.step == "results":
    st.header("📊 סיכום מבחן בדיקה")
    exam = EXAMS_DATABASE[st.session_state.current_exam_id]
    correct_count = 0
    for i, q in enumerate(exam['questions']):
        user_ans = st.session_state.exam_answers.get(i)
        correct_ans = q['options'][q['correct_idx']]
        is_correct = user_ans == correct_ans
        if is_correct: correct_count += 1
        with st.expander(f"{'✅' if is_correct else '❌'} שאלה {i+1}"):
            st.write(f"**התשובה שלך:** {user_ans if user_ans else 'לא נענתה'}")
            st.write(f"**התשובה הנכונה:** {correct_ans}")

    st.subheader(f"ציון: {(correct_count/25)*100:.0f}")
    if st.button("חזרה לתפריט"): st.session_state.step = "menu"; st.rerun()

st.markdown(f'<div class="v-footer">Version: 1225-G2 (3-Min Test)</div>', unsafe_allow_html=True)
