import streamlit as st

st.set_page_config(
    page_title="סימולטור בחינה",
    layout="wide"
)

# CSS מהודק: צ'קבוקס לימין, רווחים מינימליים
st.markdown("""
    <style>
    .block-container { 
        padding-top: 1rem; 
        max-width: 800px; 
        margin: auto; 
        direction: rtl; 
    }
    
    .stMarkdown, p, label, h1, h3 { 
        text-align: right !important; 
        direction: rtl !important;
        margin-bottom: 5px !important;
    }

    /* הצמדת הצ'קבוקס לימין המלל */
    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 10px;
        display: flex !important;
    }

    .stButton > button {
        width: 100%;
        margin-top: 10px;
    }

    hr { margin: 10px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("בחינת רישיון למתווכים במקרקעין")

st.markdown("### הוראות לנבחן:")
st.markdown("1. המבחן כולל 25 שאלות.")
st.markdown("2. זמן מוקצב: 90 דקות.")
st.markdown("3. מעבר לשאלה הבאה רק לאחר סימון תשובה.")
st.markdown("4. ניתן לחזור אחורה רק לשאלות שנענו.")
st.markdown("5. בסיום 90 דקות המבחן יינעל.")
st.markdown("6. ציון עובר: 60.")
st.markdown("7. חל איסור על שימוש בחומר עזר.")

st.divider()

# מנגנון אישור
msg = "קראתי את ההוראות ואני מוכן להתחיל בבחינה"
agree = st.checkbox(msg)

if st.button("התחל בחינה", disabled=not agree):
    st.info("הכפתור הופעל. כאן תתחיל הלוגיקה.")
