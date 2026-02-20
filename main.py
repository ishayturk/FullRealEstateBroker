import streamlit as st

st.set_page_config(
    page_title="סימולטור בחינה - דף כניסה",
    layout="wide"
)

# עיצוב RTL והתאמה לפריים
st.markdown("""
    <style>
    .block-container { 
        padding-top: 2rem; 
        max-width: 800px; 
        margin: auto; 
        direction: rtl; 
    }
    
    .stMarkdown, p, label, h1, h2, h3 { 
        text-align: right !important; 
        direction: rtl !important; 
    }

    div[data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        justify-content: flex-end !important;
        gap: 10px;
    }

    .stButton > button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("בחינת רישיון למתווכים במקרקעין")

# שבירת שורות לטקסט קצר
instr_1 = "* **מבנה המבחן:** 25 שאלות רב-ברירה."
instr_2 = "* **משך זמן:** 90 דקות (שעה וחצי)."
instr_3 = "* **ציון עובר:** 60 ומעלה."
instr_4 = "* **ניווט:** ניתן לחזור אחורה לשאלות קודמות."
instr_5 = "* **חומר עזר:** חל איסור על שימוש בחומר עזר."
instr_6 = "* **שמירה:** התשובות נשמרות אוטומטית."

st.markdown("### הוראות לנבחן:")
st.markdown(instr_1)
st.markdown(instr_2)
st.markdown(instr_3)
st.markdown(instr_4)
st.markdown(instr_5)
st.markdown(instr_6)

st.divider()

# מנגנון אישור
msg = "אני מאשר שקראתי את ההוראות ואני מוכן להתחיל"
agree = st.checkbox(msg)

if st.button("התחל בחינה", disabled=not agree):
    st.info("הכפתור הופעל. כאן תתחיל הלוגיקה.")
