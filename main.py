import streamlit as st

st.set_page_config(layout="wide")

# CSS ליישור ימין מוחלט והסרת תפריטים
st.markdown("""
    <style>
    header {visibility: hidden;}
    .block-container { 
        direction: rtl; 
        max-width: 800px; 
        margin: auto; 
        padding-top: 2rem !important;
    }
    
    .stMarkdown, p, h1, h3, label { 
        text-align: right !important; 
        direction: rtl !important;
        margin-bottom: 0px !important;
    }

    div[data-testid="stCheckbox"] {
        direction: rtl !important;
    }
    
    div[data-testid="stCheckbox"] > label {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
    }

    .stButton { text-align: right !important; }
    hr { margin: 15px 0 !important; }
    h1 { font-size: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# כותרת אחת בלבד כפי שביקשת
st.title("הוראות למבחן רישויי מקרקעין")

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
