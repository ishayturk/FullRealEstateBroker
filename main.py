elif st.session_state.step == "lesson_run":
    topic = st.session_state.selected_topic
    st.header(f"📖 {topic}")
    
    subs = SYLLABUS.get(topic, [])
    # יצירת עמודות עבור תתי הנושאים + עמודה לשאלון
    cols = st.columns(len(subs) + 1) 
    
    for i, s in enumerate(subs):
        if cols[i].button(s, key=f"sub_{i}"):
            st.session_state.update({
                "current_sub": s, "lesson_txt": "LOADING", "quiz_active": False, 
                "q_data": None, "quiz_finished": False, "q_count": 0, "correct_answers": 0
            })
            st.rerun()
    
    # הוספת כפתור השאלון בסוף השורה של תתי הנושאים
    if cols[-1].button("📝 שאלון נושא", type="primary"):
        with st.spinner("מעלה שאלה..."):
            res = fetch_q_ai(topic)
            if res:
                st.session_state.update({
                    "current_sub": f"שאלון כללי: {topic}",
                    "lesson_txt": "QUIZ_ONLY", # סימון שהגענו ישר לשאלון
                    "q_data": res, "q_count": 1, "quiz_active": True, 
                    "show_ans": False, "correct_answers": 0, "quiz_finished": False
                })
                st.rerun()

    if st.session_state.get("lesson_txt") == "LOADING":
        st.subheader(st.session_state.current_sub)
        st.session_state.lesson_txt = stream_ai_lesson(f"שיעור על {st.session_state.current_sub} בחוק {topic}")
        st.rerun()
    elif st.session_state.get("lesson_txt") and st.session_state.lesson_txt != "QUIZ_ONLY":
        st.subheader(st.session_state.current_sub)
        st.markdown(st.session_state.lesson_txt)
