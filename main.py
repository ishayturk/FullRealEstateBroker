import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 0rem 1rem !important; direction: rtl; }
    .stMarkdown p { 
        margin: 0 !important; 
        text-align: right !important; 
        line-height: 1.1 !important; 
    }
    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 5px;
        margin-top: 0 !important;
    }
    h1, h3 { margin: 0 !important; text-align: right !important; }
    hr { margin: 5px 0 !important; }
    .stButton button { width: 100%; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("בחינת רישיון למתווכים")
st.markdown("### הוראות לנבחן:")
st.markdown("1. המבחן כולל 25 שאלות.")
st.markdown("2. זמן מוקצב: 90 דקות.")
st.markdown("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
st.markdown("4. ניתן לחזור אחורה רק לשאלות שנענו.")
st.markdown("5. בסיום 90 דקות המבחן יינעל.")
st.markdown("6. ציון עובר: 60.")
st.markdown("7. חל איסור על שימוש בחומר עזר.")

st.divider()

agree = st.checkbox("קראתי את ההוראות ואני מוכן להתחיל בבחינה")

if st.button("התחל בחינה", disabled=not agree):
    st.write("נלחץ")
