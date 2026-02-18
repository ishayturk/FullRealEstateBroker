# ID: C-01
# Based on Anchor: 1218-G2
# UI: Instructions screen, responsive navigation, and full-text feedback

import streamlit as st
import time

def show_instructions():
    st.title("📄 הוראות לבחינה")
    st.write("זמן: 90 דקות | שאלות: 25 | ניווט חופשי")
    st.divider()
    if st.button("עבור/י למבחן 🚀"):
        st.session_state.start_time = time.time()
        st.session_state.step = 'exam'
        st.rerun()

def render_navigation(total_loaded, is_mobile):
    if is_mobile:
        with st.sidebar.expander("🔍 ניווט", expanded=False):
            return st.radio("שאלה:", range(1, total_loaded + 1), horizontal=True)
    return st.sidebar.radio("ניווט שאלות:", range(1, total_loaded + 1))
