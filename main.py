# ==========================================
# Project: מתווך בקליק | Version: 1231-G2
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

st.title("🏠 מתווך בקליק")

SYLLABUS = {
    "חוק המתווכים": ["רישוי והגבלות", "הגינות וזהירות", "הזמנה בכתב"],
    "חוק המקרקעין": ["בעלות וזכויות", "בתים משותפים", "הערות אזהרה"],
    "חוק החוזים": ["כריתת חוזה", "פגמים בחוזה", "תרופות"],
    "חוק התכנון והבנייה": ["היתרים", "היטל השבחה"]
}

EXAMS_DATABASE = {
    "test_exam_1": {
        "name": "מבחן בדיקה מהיר",
        "questions": [{"q": f"שאלה לדוגמה {i+1}: מהו המלל הנכון?", 
                       "options": ["תשובה א' המלאה", "תשובה ב' המלאה", "תשובה ג' המלאה", "תשובה ד' המלאה"], 
                       "correct_idx": 0} for i in range(25)]
    }
}

def stream_ai_lesson(p):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        res = m.generate_content(p, stream=True)
        ph = st.empty(); txt = ""
        for chunk in res:
            txt += chunk.text
            ph.markdown(txt + "▌")
        ph.markdown(txt)
        return txt
    except: return "⚠️ תקלה בחיבור ל-AI."

if "step" not in st.session_state:
    st.session_state.update({
        "user": None, "step": "login", "used_exams": [], 
        "current_exam_id": None, "exam_qs": [], "current_q_idx": 0, 
        "max_reached_idx": 0, "exam_answers": {}, "start_time": None,
        "show_nav": False, "lesson_txt": "", "selected_topic": None, "current_sub": None
    })

if st.session_state.step == "login":
    u = st.text_input("שם מלא:")
    if st.button("כניסה") and u:
        st.session_state.update({"user": u, "step": "menu"}); st.rerun()

elif st.session_state.step == "menu":
    st.subheader(f"👤 שלום, {st.session_state.user}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📚 לימוד לפי נושאים"): 
            st.session_state.step = "study"; st.rerun()
    with c2:
        if st.button("⏱️ גש למבחן מלא"): 
            st.session_state.step = "exam_prep"; st.rerun()

elif st.session_state.step == "study":
    st.subheader("📚 בחר נושא ללימוד")
    sel = st.selectbox("בחר נושא מרשימת הסילבוס:", ["בחר נושא"] + list(SYLLABUS.keys()))
    if sel != "בחר נושא":
        st.session_state.selected_topic = sel
        subs = SYLLABUS[sel]
        cols = st.columns(len(subs))
        for i, s in enumerate(subs):
            if cols[i].button(s):
                st.session_state.current_sub = s
                st.session_state.step = "lesson_run"
                st.session_state.lesson_txt = "LOADING"; st.rerun()
    if st.button("🏠 חזרה לתפריט"): st.session_state.step = "menu"; st.rerun()

elif st.session_state.step == "lesson_run":
    st.header(f"📖 {st.session_state.current_sub}")
    if st.session_state.lesson_txt == "LOADING":
        st.session_state.lesson_txt = stream_ai_lesson(f"כתוב שיעור מקיף ומקצועי על {st.session_state.current_sub} כהכנה למבחן המתווכים.")
    else:
        st.markdown(st.session_state.lesson_txt)
    if st.button("⬅️ חזרה לבחירת נושא"): 
        st.session_state.step = "study"; st.session_state.lesson_txt = ""; st.rerun()

elif st.session_state.step == "exam_prep":
    st.header("📝 הכנה למבחן")
    if not st.session_state.exam_qs:
        st.session_state.exam_qs = EXAMS_DATABASE["test_exam_1"]["questions"][:5]
    if st.button("🚀 התחל מבחן"):
        st.session_state.update({"current_exam_id": "test_exam_1", "step": "exam_run", "start_time": time.time()})
        st.rerun()

elif st.session_state.step == "exam_run":
    elapsed = time.time() - st.session_state.start_time
    rem = max(0, 180 - int(elapsed))
    if rem <= 0: st.session_state.step = "time_up"; st.rerun()
    mins, secs = divmod(rem, 60)
    st.markdown(f'<div class="timer-box">⏳ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

    if st.button("📱 לוח ניווט"): st.session_state.show_nav = not st.session_state.show_nav
    if st.session_state.show_nav:
        st.markdown('<div class="nav-overlay">', unsafe_allow_html=True)
        cols = st.columns(5)
        for i in range(25):
            with cols[i%5]:
                if i > st.session_state.max_reached_idx: st.button(f"🔒 {i+1}", key=f"n_{i}", disabled=True)
                else:
                    lbl = f"{i+1} {'✅' if i in st.session_state.exam_answers else ''}"
                    if st.button(lbl, key=f"n_{i}"):
                        st.session_state.current_q_idx = i; st.session_state.show_nav = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    idx = st.session_state.current_q_idx
    q = st.session_state.exam_qs[idx]
    st.subheader(f"שאלה {idx + 1}")
    curr_ans = st.session_state.exam_answers.get(idx)
    ans = st.radio(q['q'], q['options'], index=None if curr_ans is None else q['options'].index(curr_ans), key=f"r_{idx}")
    if ans: st.session_state.exam_answers[idx] = ans

    c1, c2, c3 = st.columns(3)
    with c1:
        if idx > 0 and st.button("⬅️ הקודם", key="prev_btn"): 
            st.session_state.current_q_idx -= 1; st.rerun()
    with c2:
        if st.button("🏁 הגש", key="submit_btn"): 
            st.session_state.step = "results"; st.rerun()
    with c3:
        if idx < 24 and st.button("הבא ➡️", key="next_btn"):
            if idx == st.session_state.max_reached_idx: st.session_state.max_reached_idx += 1
            if idx == len(st.session_state.exam_qs)-1:
                st.session_state.exam_qs += EXAMS_DATABASE["test_exam_1"]["questions"][idx+1:idx+6]
            st.session_state.current_q_idx += 1; st.rerun()

elif st.session_state.step == "time_up":
    st.error("⌛ נגמר הזמן!"); st.button("צפה בתוצאות", on_click=lambda: st.session_state.update({"step":"results"}))

elif st.session_state.step == "results":
    st.header("📊 תוצאות")
    exam = EXAMS_DATABASE[st.session_state.current_exam_id]
    corrects = 0
    for i, q in enumerate(exam['questions']):
        u_ans = st.session_state.exam_answers.get(i)
        c_ans = q['options'][q['correct_idx']]
        is_ok = (u_ans == c_ans)
        if is_ok: corrects += 1
        with st.expander(f"{'✅' if is_ok else '❌'} שאלה {i+1}"):
            st.write(f"**התשובה שלך:** {u_ans if u_ans else 'לא נענתה'}")
            st.write(f"**התשובה הנכונה:** {c_ans}")
    st.subheader(f"ציון: {(corrects/25)*100:.0f}")
    if st.button("חזרה לתפריט"): st.session_state.step = "menu"; st.rerun()

st.markdown(f'<div class="v-footer">Version: 1231-G2</div>', unsafe_allow_html=True)
