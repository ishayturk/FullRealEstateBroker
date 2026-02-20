# --- בתוך main.py ---
st.markdown(f"""
<style>
    /* ... שאר ה-CSS ... */

    /* עיצוב מעודכן לכפתור בתוך הסטריפ - קטן ואסתטי */
    .stLinkButton > a {{
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        border-radius: 8px !important; 
        font-weight: bold !important; 
        background-color: transparent !important;
        color: #31333f !important;
        border: 1px solid #d1d5db !important;
        text-decoration: none !important;
        transition: 0.2s;
        padding: 4px 12px !important; /* קטן יותר */
        font-size: 0.85rem !important; /* עדין יותר */
        height: 32px !important; /* גובה קבוע לסטריפ */
    }}
</style>
""", unsafe_allow_html=True)
