import streamlit as st
import google.generativeai as genai
import json, re, time

# הגדרות עמוד ויישור לפי ה-DNA של גרסה 1213
st.set_page_config(page_title="מתווך בקליק - בחינה", layout="wide")

st.markdown("""
<style>
    /* יישור גלובלי לימין */
    * { direction: rtl; text-align: right; }
    
    /* כפתורים בעיצוב המערכת המוכרת */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 3em; }
    
    /* עיצוב שאלה */
    .question-box { font-size: 1.5rem !important; font-weight: bold; margin-bottom: 20px; }
    
    /* רדיו באטן - נקודה מימין למלל (קריטי!) */
    [data-testid="stRadio"] div[role="radiogroup"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 15px !important;
        font-size: 1.2rem !important;
    }
    
    /* צ'קבוקס הסבר - ריבוע מימין למלל עם רווח */
    [data-testid="stCheckbox"] label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 30px !important;
    }

    .v-footer { text-align: center; color: rgba(255, 255, 255, 0.1); font-size: 0.7em; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# פונקציית ייצור שאלה (Gemini) - מבוסס על המנגנון ב-1213
def fetch_exam_q_ai():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = "צור שאלה אמריקאית קשה בנושא אתיקה מקצועית למבחן המתווכים. החזר אך ורק JSON תקני: {'q':'','options':['','','',''],'correct_idx':int}"
        res = model.generate_content(prompt).text
        match = re.search(r'\{.*\}', res, re.DOTALL)
        if match: return json.loads(match.group())
    except: return None
    return None

# ניהול State
if "exam" not in st.session_state:
    st.session_state.exam = {
        "step": "instructions",
        "questions": [],
        "current_idx": 0,
        "answers": {},
        "start_time": None,
        "is_finished": False
    }

ex = st.session_state.exam

# --- עמוד הסבר ---
if ex["step"] == "instructions":
    st.title("🏠 בחינת הסמכה - אתיקה")
    st.header("הוראות לנבחן")
    st.write("לפניך סימולציה של 5 שאלות. הזמן המוקצב הוא 5 דקות.")
    
    # צ'קבוקס מיושר לימין עם רווח
    agreed = st.checkbox("קראתי והבנתי את ההוראות לבחינה")
    
    if st.button("התחל בחינה"):
        if agreed:
            with st.spinner("מייצר שאלות..."):
                q = fetch_exam_q_ai()
                if q:
                    ex["questions"] = [q]
                    ex["step"] = "running"
                    ex["start_time"] = time.time()
                    st.rerun()
        else:
            st.warning("עליך לאשר את ההוראות.")

# --- עמוד בחינה פעיל ---
elif ex["step"] == "running" and not ex["is_finished"]:
    # חישוב זמן שקט (מתעדכן רק בפעולות)
    elapsed = time.time() - ex["start_time"]
    remaining = max(0, 300 - int(elapsed))
    
    if remaining <= 0:
        ex["is_finished"] = True
        st.rerun()

    # Sidebar: טיימר וניווט
    with st.sidebar:
        st.markdown(f"### ⏳ זמן נותר: {remaining // 60}:{remaining % 60:02d}")
        st.divider()
        st.write("### ניווט (4 בשורה)")
        
        # גריד כפתורים 4 בשורה
        for r in range(2):
            cols = st.columns(4)
            for c in range(4):
                idx = r * 4 + c
                if idx < 5:
                    is_curr = (idx == ex["current_idx"])
                    if cols[c].button(f"{idx+1}", key=f"n_{idx}", type="primary" if is_curr else "secondary"):
                        while len(ex["questions"]) <= idx:
                            new_q = fetch_exam_q_ai()
                            if new_q: ex["questions"].append(new_q)
                        ex["current_idx"] = idx
                        st.rerun()

    # תצוגת השאלה
    q = ex["questions"][ex["current_idx"]]
    st.markdown(f"<div class='question-box'>שאלה {ex['current_idx'] + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-box'>{q['q']}</div>", unsafe_allow_html=True)
    
    # רדיו באטן - נקודה מימין
    user_ans = ex["answers"].get(ex["current_idx"], None)
    choice = st.radio("", q['options'], index=user_ans, key=f"rad_{ex['current_idx']}", label_visibility="collapsed")
    
    if choice is not None:
        ex["answers"][ex["current_idx"]] = q['options'].index(choice)

    st.divider()
    
    # כפתורי שליטה: [הבא] [הגש] [הקודם]
    c_next, c_finish, c_prev = st.columns([1,1,1])
    
    with c_prev:
        if ex["current_idx"] > 0:
            if st.button("שאלה קודמת ➡️"):
                ex["current_idx"] -= 1
                st.rerun()
                
    with c_finish:
        # הגש מופיע רק בשאלה האחרונה (5)
        if ex["current_idx"] == 4:
            if st.button("🏁 הגש מבחן", type="primary"):
                ex["is_finished"] = True
                st.rerun()

    with c_next:
        if ex["current_idx"] < 4:
            has_ans = ex["current_idx"] in ex["answers"]
            # הבא חסום עד שעונים
            if st.button("⬅️ שאלה הבאה", disabled=not has_ans):
                ex["current_idx"] += 1
                if len(ex["questions"]) <= ex["current_idx"]:
                    with st.spinner("טוען שאלה..."):
                        new_q = fetch_exam_q_ai()
                        if new_q: ex["questions"].append(new_q)
                st.rerun()

# --- עמוד סיום נקי (כפי שביקשת) ---
else:
    st.header("🏁 סיום בחינה")
    st.divider()
    st.subheader(f"ענית על {len(ex['answers'])} שאלות מתוך 5.")
    st.write("הבחינה הסתיימה בהצלחה.")
    
    if st.button("חזרה לתפריט"):
        st.session_state.clear()
        st.rerun()

st.markdown(f'<div class="v-footer">Version: 1213-Main</div>', unsafe_allow_html=True)
