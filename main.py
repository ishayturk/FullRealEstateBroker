import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* ביטול רווחים עליונים וצמצום המכל */
    .block-container { 
        padding: 0rem !important; 
        max-width: 700px; 
        margin: auto; 
    }
    
    /* יישור טקסט וצמצום מרווח בין שורות */
    .stMarkdown, p, h1, h3, label { 
        text-align: right !important; 
        direction: rtl !important;
        margin-bottom: 0px !important;
        padding-bottom: 2px !important;
    }

    /* הצמדת הצ'קבוקס לימין המוחלט */
    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 8px;
        margin-top: 5px !important;
    }

    /* התאמת הכפתור */
    .stButton button { 
        width: 100%; 
        margin-top: 5px !important; 
    }
    
    hr { margin: 5px 0 !important; }
    h1 { font-size: 1.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("בחינת רישיון למתווכים")

st.markdown("### הוראות:")
st.write("1. 25 שאלות | 90 דקות.")
st.write("2. מעבר לשאלה הבאה רק לאחר מענה.")
st.write("3. ניתן לחזור אחורה לשאלות שנענו.")
st.write("4. ציון עובר: 60.")
st.write("5. חל איסור על שימוש בחומר עזר.")

st.divider()

agree = st.checkbox("אני מאשר את ההוראות ומוכן להתחיל")

if st.button("התחל בחינה", disabled=not agree):
    pass
