import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .block-container { 
        direction: rtl; 
        max-width: 800px; 
        margin: auto; 
        padding-top: 0.5rem !important;
    }
    .stMarkdown, p, h1, h3, label { 
        text-align: right !important; 
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 10px;
        margin-top: 5px !important;
    }
    .stButton { text-align: right !important; }
    hr { margin: 8px 0 !important; }
    h1 { font-size: 1.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

# כותרת בשורה אחת
st.title("בחינת רישיון למתווכים במקרקעין")

st.markdown("### הוראות לנבחן:")
st.write("1. המבחן כולל 25 שאלות.")
st.write("2. זמן מוקצב: 90 דקות.")
st.write("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
st.write("4. ניתן לחזור אחורה רק לשאלות שנענו.")
st.write("5. בסיום 90 דקות המבחן יינעל.")
st.write("6. ציון עובר: 60.")
st.write("7. חל איסור על שימוש בחומר עזר.")

st.divider()

msg = "קראתי את ההוראות ואני מוכן להתחיל בבחינה"
agree = st.checkbox(msg)

if st.button("התחל בחינה", disabled=not agree):
    pass
