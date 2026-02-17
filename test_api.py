import streamlit as st
import google.generativeai as genai

st.title("בדיקת חיבור ל-API")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ המפתח GEMINI_API_KEY לא נמצא ב-Secrets של סטרימליט!")
else:
    key = st.secrets["GEMINI_API_KEY"]
    st.write(f"מפתח זוהה (4 תווים אחרונים): ****{key[-4:]}")
    
    try:
        genai.configure(api_key=key)
        models = genai.list_models()
        st.success("✅ הצלחתי להתחבר לגוגל! אלו המודלים שזמינים לך:")
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name)
    except Exception as e:
        st.error(f"❌ שגיאה בהתחברות לגוגל: {e}")
