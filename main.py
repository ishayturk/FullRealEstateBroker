# ==========================================
# Project: מתווך בקליק | Version: 1234-G2
# ==========================================
import streamlit as st
import time

st.set_page_config(page_title="מתווך בקליק", layout="wide")

# CSS בסיסי בלבד לטיימר וניווט
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .timer-box {
        position: fixed; top: 10px; left: 10px; background: #ff4b4b; color: white;
        padding: 8px; border-radius: 8px; z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# אתחול State
if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login",
        "exam_qs": [], "current_q_idx": 0, "max_reached_idx": 0,
        "exam_answers": {}, "start_time": None
    })

# מאגר בדיקה (25 שאלות)
TEST_EXAM = [{"q": f"שאלה לבדיקה {i+1}", "options": ["תשובה 1", "תשובה 2", "תשובה 3", "תשובה 4"], "correct_idx": 0} for i in range(25)]

# --- שלב 1: כניסה ---
if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.user = u
        st.session_state.step = "menu"; st.rerun()

# --- שלב 2: תפריט ---
elif st.session_state.step == "menu":
    st.write(f"שלום, {st.session_state.user}")
    if st.button("⏱️ גש למבחן מלא (3 דקות לבדיקה)"):
        st.session_state.update({
            "step": "exam_run", "start_time": time.time(),
            "exam_qs": TEST_EXAM[:5], "exam_answers": {}, 
            "current_q_idx": 0, "max_reached_idx": 0
        })
        st.rerun()

# --- שלב 3: הרצת מבחן ---
elif st.session_state.step == "exam_run":
    # טיימר בדיקה - 180 שניות
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 180 - int(elapsed))
    if rem <= 0: st.session_state.step = "results"; st.rerun()
    
    mins, secs = divmod(rem, 60)
    st.markdown(f'<div class="timer-box">⏳ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    idx = st.session_state.current_q_idx
    q = st.session_state.exam_qs[idx]
    
    st.subheader(f"שאלה {idx + 1}")
    curr_val = st.session_state.exam_answers.get(idx)
    ans = st.radio(q['q'], q['options'], index=None if curr_val is None else q['options'].index(curr_val), key=f"q_{idx}")
    if ans: st.session_state.exam_answers[idx] = ans

    c1, c2 = st.columns(2)
    with c1:
        if idx > 0 and st.button("⬅️ הקודם"): 
            st.session_state.current_q_idx -= 1; st.rerun()
    with c2:
        if idx < 24:
            if st.button("הבא ➡️"):
                if idx == st.session_state.max_reached_idx: st.session_state.max_reached_idx += 1
                if idx == len(st.session_state.exam_qs)-1:
                    st.session_state.exam_qs += TEST_EXAM[idx+1:idx+6]
                st.session_state.current_q_idx += 1; st.rerun()
        else:
            if st.button("🏁 הגש מבחן"): st.session_state.step = "results"; st.rerun()

# --- שלב 4: תוצאות (סיכום מילולי) ---
elif st.session_state.step == "results":
    st.header("📊 סיכום מבחן")
    corrects = 0
    for i, q in enumerate(TEST_EXAM):
        u_ans = st.session_state.exam_answers.get(i)
        c_ans = q['options'][q['correct_idx']]
        is_correct = (u_ans == c_ans)
        if is_correct: corrects += 1
        
        with st.expander(f"{'✅' if is_correct else '❌'} שאלה {i+1}"):
            st.write(f"**התשובה שלך:** {u_ans if u_ans else 'לא ענית'}")
            st.write(f"**התשובה הנכונה:** {c_ans}")
    
    st.subheader(f"ציון: {(corrects/25)*100:.0f}")
    if st.button("חזרה לתפריט"): st.session_state.step = "menu"; st.rerun()
