import streamlit as st

st.set_page_config(layout="wide")

# הסרת תפריטים וסידור מרווחים
st.markdown("""
    <style>
    /* הסרת התפריט העליון והלוגו של Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    .block-container { 
        direction: rtl; 
        max-width: 800px; 
        margin: auto; 
        padding-top: 2rem !important;
    }
    
    .stMarkdown, p, h1, h3, label { 
        text-align: right !important; 
        margin-bottom: 0px !important;
        line-height: 1.2 !important;
    }

    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 10px;
        margin-top: 10px !important;
    }

    .stButton { text-align: right !important; }
    hr { margin: 15px 0 !important; }
    </style>
    """, unsafe_allow_html=True)

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
