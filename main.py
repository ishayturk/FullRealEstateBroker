# Project: מתווך בקליק - מערכת בחינות | File: main.py
# Claude 23 | Finish button outside is_time_up block
import streamlit as st
import logic
import streamlit.components.v1 as components

st.set_page_config(page_title="מתווך בקליק", layout="wide", initial_sidebar_state="collapsed")
user_name = st.query_params.get("user", "אורח")

st.markdown("""
    <style>
    /* --- SECTION: GENERAL --- */
    * { direction: rtl; text-align: right; }
    header, #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 1100px !important; margin: 0 auto !important; padding-top: 0.5rem !important; }
    .header-box { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 8px; }

    /* --- SECTION: DESKTOP --- */
    @media (min-width: 769px) {
        .nav-title { display: block; margin-bottom: 10px; font-weight: bold; }
        .question-area { padding-right: 8%; padding-left: 8%; }
        .mobile-header { display: none !important; }
        [data-testid="column"]:last-child { margin-left: -6ch !important; }
        [data-testid="stRadio"] { margin-bottom: 0.3rem !important; }
    }

    /* --- SECTION: MOBILE --- */
    @media (max-width: 768px) {
        .block-container { padding-top: 60px !important; }
        .mobile-up { margin-top: 0px !important; }
        .nav-title { margin-top: 10px !important; text-align: center; display: block; }
        iframe { width: 100% !important; height: 50px !important; }
        .desktop-header { display: none !important; }
        .mobile-header {
            display: flex !important;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 0;
            width: fit-content;
            margin: 4px auto 4px auto;
            font-size: 1.1rem;
            font-weight: bold;
        }
        .mobile-header-spacer {
            display: inline-block;
            width: 3em;
        }
        /* שינוי טקסט כפתורים בנייד */
        #btn_next button p { font-size: 0; }
        #btn_next button p::before { content: "הבאה"; font-size: 1rem; }
        #btn_prev button p { font-size: 0; }
        #btn_prev button p::before { content: "הקודמת"; font-size: 1rem; }
    }
    </style>
""", unsafe_allow_html=True)

# --- אתחול ---
logic.initialize_exam_state()

# --- טעינת בחינה בפעם הראשונה ---
if not st.session_state.get("exam_file"):
    logic.load_exam()
    st.rerun()


# --- סטריפ עליון מחשב ---
h1, h2, h3 = st.columns([2, 1, 2])
with h1: st.markdown(f'<div class="desktop-header" style="text-align: left; font-weight: bold; font-size: 1.1rem;">🏠 מתווך בקליק</div>', unsafe_allow_html=True)
with h2: st.markdown('<div class="desktop-header" style="text-align: center; color: #eee;">|</div>', unsafe_allow_html=True)
with h3: st.markdown(f'<div class="desktop-header" style="text-align: right; font-weight: bold;">👤 {user_name}</div>', unsafe_allow_html=True)
st.markdown('<div class="header-box desktop-header"></div>', unsafe_allow_html=True)

# --- סטריפ עליון נייד ---
st.markdown(f"""
    <div class="mobile-header">
        <div style="white-space:nowrap;">🏠 מתווך בקליק</div>
        <div class="mobile-header-spacer"></div>
        <div style="white-space:nowrap;">👤 {user_name}</div>
    </div>
""", unsafe_allow_html=True)

current_step = st.session_state.get("step", "instructions")

# זיהוי לחיצת סיים בחינה מה-iframe
if st.query_params.get("finish") == "1":
    st.session_state.step = "feedback"
    st.rerun()

# ===== דף הוראות =====
if current_step == "instructions":
    components.html("<script>localStorage.removeItem('exam_timeout');</script>", height=0)
    st.markdown('<h2 style="text-align: center;">הוראות למבחן רישוי מתווכים</h2>', unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        instructions = [
            "המבחן כולל 25 שאלות.",
            "זמן מוקצב: 90 דקות.",
            "מעבר לשאלה הבאה רק לאחר סימון תשובה.",
            "ניתן לחזור אחורה לשאלות שנחשפו.",
            "ציון עובר: 60.",
        ]
        for i, txt in enumerate(instructions, 1):
            st.write(f"{i}. {txt}")
        st.write("")
        f_cols = st.columns([1, 1])
        with f_cols[0]:
            agree = st.checkbox("קראתי את ההוראות")
        with f_cols[1]:
            q1_ready = st.session_state.get("q1_ready", False)
            start_disabled = not (agree and q1_ready)
            if st.button("התחל בחינה", disabled=start_disabled):
                import time
                st.session_state.step = "exam_run"
                st.session_state.current_q = 1
                st.session_state.nav_active_questions.add(1)
                st.session_state.exam_start_time = time.time()
                logic.ensure_question_exists(2)
                st.rerun()

# ===== מהלך הבחינה =====
elif current_step == "exam_run":
    rem_sec = logic.get_remaining_seconds()
    header_html = f"""
    <style>
        body {{ margin:0; padding:0; overflow:hidden; }}
        .wrapper {{
            direction: rtl; display: flex; align-items: center; justify-content: center; width: 100%;
            margin-top: 4px; margin-bottom: 4px;
        }}
        .t-text {{ font-size: 2.2rem; font-weight: bold; color: #000; white-space: nowrap; }}
        .c-text {{ font-size: 2rem; font-weight: bold; margin-right: 30px; direction: ltr; }}
        #timeout-msg {{ display:none; direction:rtl; text-align:right; padding: 8px 0; }}
        @media (max-width: 768px) {{
            .wrapper {{ gap: 15px !important; margin-top: 2px !important; margin-bottom: 2px !important; }}
            .t-text {{ font-size: 1rem !important; }}
            .c-text {{ font-size: 1rem !important; margin-right: 0 !important; }}
        }}
    </style>
    <div class="wrapper">
        <div class="t-text">מבחן רישוי למתווכים</div>
        <div id="clock-val" class="c-text"></div>
    </div>
    <div id="timeout-msg">
        <span style="font-size:0.9rem; font-weight:bold; color:#cc0000;">זמן הבחינה תם — אנא לחץ על הכפתור</span>
        &nbsp;
        <button onclick="parent.location.href=parent.location.pathname+'?finish=1'"
            style="background:#ff4b4b; color:white; border:none; padding:6px 18px; border-radius:6px; font-size:0.9rem; cursor:pointer; font-weight:bold;">
            סיים בחינה
        </button>
    </div>
    <script>
    var s = {rem_sec};
    function u() {{
        var m = Math.floor(s / 60); var sec = s % 60;
        var el = document.getElementById('clock-val');
        if (el) {{
            el.innerHTML = (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
            if (s <= 600) el.style.color = "red";
        }}
        if (s <= 0) {{
            document.getElementById('timeout-msg').style.display = 'block';
            // הרחב את ה-iframe
            try {{
                var frames = parent.document.querySelectorAll('iframe');
                frames.forEach(function(f) {{
                    if (f.contentWindow === window) f.style.height = '90px';
                }});
            }} catch(e) {{}}
            return;
        }}
        s--;
    }}
    u(); setInterval(u, 1000);
    </script>
    """
    components.html(header_html, height=50)

    is_time_up = st.query_params.get("timeout") == "1" or st.session_state.get("timed_out", False)
    if is_time_up:
        st.session_state.timed_out = True

    col_main, col_nav = st.columns([2.5, 1], gap="medium")
    with col_main:
        st.markdown('<div id="question-area" class="question-area" style="margin-top:8px;">', unsafe_allow_html=True)

        if is_time_up:
            st.markdown('<p style="color: #888; font-weight: bold; font-size: 1.1rem; margin-bottom: 2px;">זמן הבחינה תם</p>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.9rem; font-weight:bold; margin-bottom:15px;">נא ללחוץ על סיים בחינה</div>', unsafe_allow_html=True)
            if st.button("**סיים בחינה**", type="primary", key="btn_finish_timeout"):
                st.session_state.step = "feedback"
                st.rerun()
        else:
            idx = st.session_state.current_q
            q = st.session_state.exam_questions.get(idx)

            if q:
                st.markdown(f'<p style="color: #888; font-weight: bold; font-size: 1.1rem; margin-bottom: 2px;">שאלה {idx}</p>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.9rem; font-weight:bold; margin-bottom:15px;">{q["text"]}</div>', unsafe_allow_html=True)

                options_dict = q.get("options", {})
                options_labels = list(options_dict.keys())
                options_list = [f"{k}. {v}" for k, v in options_dict.items()]

                existing_label = st.session_state.user_answers.get(idx, {}).get("label", None)
                existing_index = options_labels.index(existing_label) if existing_label in options_labels else None

                chosen = st.radio("", options_list, index=existing_index, key=f"r_{idx}", label_visibility="collapsed")

                if chosen is not None:
                    chosen_label = options_labels[options_list.index(chosen)]
                    logic.record_answer(idx, chosen_label)
                    if idx == 25:
                        st.session_state.finish_button_visible = True

                st.markdown('<div class="btn-area"></div>', unsafe_allow_html=True)

                b_n, b_p, b_f = st.columns([1, 1, 1.2])
                with b_n:
                    if idx < 25:
                        next_ready = (idx + 1) in st.session_state.exam_questions
                        has_answer = idx in st.session_state.user_answers
                        if st.button("לשאלה הבאה", key="btn_next", disabled=not (has_answer and next_ready)):
                            st.session_state.current_q += 1
                            st.session_state.nav_active_questions.add(st.session_state.current_q)
                            if idx <= 23:
                                logic.ensure_question_exists(idx + 2)
                            st.rerun()
                with b_p:
                    if idx > 1:
                        if st.button("לשאלה הקודמת", key="btn_prev"):
                            st.session_state.current_q -= 1
                            st.rerun()
                with b_f:
                    if st.session_state.get("finish_button_visible"):
                        if st.button("**סיים בחינה**", type="primary", key="btn_finish"):
                            st.session_state.step = "feedback"
                            st.rerun()
            else:
                st.info("טוען שאלה...")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_nav:
        st.markdown('<div class="nav-title">מפת שאלות:</div>', unsafe_allow_html=True)
        for r in range(0, 25, 4):
            cols = st.columns(4)
            for i in range(4):
                n = r + i + 1
                if n <= 25:
                    is_active = n in st.session_state.nav_active_questions
                    label = f"**{n}**" if n == st.session_state.current_q else str(n)
                    if cols[i].button(label, key=f"n_{n}", disabled=not is_active):
                        st.session_state.current_q = n
                        st.rerun()

# ===== משוב =====
elif current_step == "feedback":
    score = logic.get_total_score()
    correct_count = sum(1 for n in range(1, 26) if logic.get_points(n) == 4)
    score_color = "#1a7a1a" if score >= 60 else "#cc0000"

    st.markdown(f"""
        <div style="border-bottom: 1px solid #eee; padding-bottom: 6px; margin-bottom: 16px;">
            <p style="font-size:1rem; margin:0;">
                ענית על <strong>{correct_count}</strong> שאלות נכון.
                ציונך הוא: <strong style="color:{score_color}; font-size:1.2rem;">{score}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

    for n in range(1, 26):
        q = st.session_state.exam_questions.get(n)
        if not q:
            continue
        user = st.session_state.user_answers.get(n, {})
        user_label = user.get("label", None)
        correct_label = q.get("correct_label", "")
        correct_text = q.get("options", {}).get(correct_label, "")

        if user_label is None:
            # לא נענה
            st.markdown(f"""
                <div style="background:#f5f5f5; border-radius:8px; padding:12px; margin-bottom:10px;">
                    <p style="font-weight:bold; margin-bottom:6px;">⬜ שאלה {n} — {q['text']}</p>
                    <p style="margin:2px 0; color:#888;">לא נענה</p>
                    <p style="margin:2px 0; color:#cc0000;">תשובה נכונה: {correct_label}. {correct_text}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            user_text = q.get("options", {}).get(user_label, "")
            is_correct = logic.get_points(n) == 4
            mark = "✅" if is_correct else "❌"
            bg = "#f0fff0" if is_correct else "#fff0f0"
            st.markdown(f"""
                <div style="background:{bg}; border-radius:8px; padding:12px; margin-bottom:10px;">
                    <p style="font-weight:bold; margin-bottom:6px;">{mark} שאלה {n} — {q['text']}</p>
                    <p style="margin:2px 0;">תשובתך: {user_label}. {user_text}</p>
                    {"" if is_correct else f'<p style="margin:2px 0; color:#cc0000;">תשובה נכונה: {correct_label}. {correct_text}</p>'}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("בחינה חדשה"):
        for key in ["step","current_q","exam_questions","user_answers",
                    "nav_active_questions","finish_button_visible","exam_start_time",
                    "exam_file","_exam_raw","q1_ready","timed_out"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
# סוף קובץ
