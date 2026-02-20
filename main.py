import streamlit as st

st.set_page_config(page_title="סימולטור בחינה - דף כניסה", layout="wide")

# עיצוב RTL והתאמה לפריים (Iframe)
st.markdown("""
    <style>
    .block-container { 
        padding-top: 2rem; 
        max-width: 800px; 
        margin: auto; 
        direction: rtl; 
    }
    
    /* יישור טקסט וכותרות לימין */
    .stMarkdown, p, label, h1, h2, h3 { 
        text-align: right !important; 
        direction: rtl !important; 
    }

    /* התאמת צ'קבוקס - סימון מימין למלל */
    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 10px;
    }

    /* עיצוב כפתור רחב */
    .stButton > button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# כותרת הדף
st.title("בחינת רישיון למתווכים במקרקעין")

# תוכן ההסבר
st.markdown("""
### הוראות לנבחן:
* **מבנה המבחן:** 25 שאלות רב-ברירה (אמריקאיות).
* **משך זמן:** 90 דקות (שעה וחצי).
* **ציון עובר:** 60 ומעלה.
* **ניווט:** ניתן לחזור אחורה לשאלות קודמות במהלך המבחן.
* **חומר עזר:** חל איסור מוחלט על שימוש בחומר עזר מכל סוג שהוא.
* **שמירה:** התשובות נשמרות באופן אוטומטי עם המעבר לשאלה הבאה.

---
""")

# מנגנון אישור ותחילת בחינה
agree = st.checkbox("אני מאשר שקראתי את ההוראות ואני מוכן להתחיל בבחינה")

# הכפתור פעיל רק אם הצ'קבוקס מסומן. כרגע הוא לא מוביל לשום מקום.
if st.button("התחל בחינה", disabled=not agree):
    st.info("הכפתור הופ
