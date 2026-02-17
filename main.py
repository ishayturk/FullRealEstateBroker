# ==========================================
# Project: מתווך בקליק | Version: 1245-G2
# ==========================================

def stream_ai_lesson(p):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        m = genai.GenerativeModel('gemini-2.0-flash')
        
        # הפרומפט המדויק מהגרסה העובדת:
        full_prompt = (
            f"הסבר באופן מקצועי וממוקד למתווכי מקרקעין על: {p}. "
            f"מיד לאחר ההסבר, צור 'שאלון חזרה מהיר' הכולל 10 שאלות אמריקאיות "
            f"קצרות ונקודתיות שבוחנות את הבנת החומר שנלמד כרגע. "
            f"בסוף, הצג מפתח תשובות ברור."
        )
        
        res = m.generate_content(full_prompt, stream=True)
        ph = st.empty(); txt = ""
        for chunk in res:
            txt += chunk.text
            ph.markdown(txt + "▌")
        ph.markdown(txt)
        return txt
    except Exception as e:
        return f"⚠️ תקלה בחיבור ל-AI: {str(e)}"
