# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V208 | Date: 23/02/2026 | 23:59
import streamlit as st
import time
import json

# פונקציית עזר ליצירת שאלה מהמנוע (סימולציה של קריאה ל-LLM עם הפרומפט המעודכן)
def generate_question_from_engine(q_num):
    """
    מייצר שאלה אחת בפורמט JSON פנימי על בסיס חומרי הלימוד (דיני מתווכים, אתיקה ועוגן 1213).
    הפרומפט מחייב: סיפור מקרה, רמה גבוהה, נימוק משפטי ותשובה נכונה אחת.
    """
    # כאן תבוא הקריאה ל-API של המודל עם הפרומפט המפורט שסיכמנו
    # לצורך הדגמה בגרסה V208, אני מייצר מבנה שתואם בדיוק את הסטנדרט של רשם המתווכים:
    
    # הערה: המנוע יקבל את הלינקים והעוגן כמקור ידע בלעדי.
    
    # דוגמה לשאלה שתיווצר (הפורמט שיישמר ב-session_state):
    sample_question = {
        "question": f"שאלה {q_num}: שמעון המתווך החתים את לקוחו על טופס הזמנת שירותי תיווך במקרקעין למכירת דירת מגורים בבלעדיות. בטופס צוין כי תקופת הבלעדיות היא ל-8 חודשים. המתווך ביצע שתי פעולות שיווק כנדרש בתקנות בתוך חודש מהחתימה. לאחר 7 חודשים נמכרה הדירה דרך מתווך אחר. האם שמעון זכאי לדמי תיווך?",
        "options": [
            "כן; מכיוון שבוצעו פעולות השיווק הנדרשות והמכירה בוצעה בתוך תקופת הבלעדיות המוסכמת.",
            "לא; תקופת הבלעדיות המקסימלית לדירת מגורים היא 6 חודשים, ולכן הבלעדיות פקעה לפני המכירה.",
            "כן; בתנאי ששמעון היה הגורם היעיל בעסקה בלבד, ללא קשר לתקופת הבלעדיות.",
            "לא; מתווך זכאי לדמי תיווך בבלעדיות רק אם ביצע לפחות 3 פעולות שיווק שונות."
        ],
        "answer_index": 1  # התשובה הנכונה לפי חוק המתווכים (תקופת בלעדיות מקסימלית)
    }
    return sample_question

def initialize_exam_state():
    """אתחול משתני הסשן בטעינה ראשונה"""
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}  # ה-Buffer של השאלות
    if "answers_user" not in st.session_state:
        st.session_state.answers_user = {}
    if "nav_active_questions" not in st.session_state:
        st.session_state.nav_active_questions = set()
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "current_q" not in st.session_state:
        st.session_state.current_q = 1
    if "finish_button_visible" not in st.session_state:
        st.session_state.finish_button_visible = False

def ensure_question_exists(q_num):
    """
    לוגיקת ה-Buffer החכמה:
    בודק אם השאלה כבר קיימת בזיכרון. אם לא, מייצר אותה.
    מוודא שלא חורגים מ-25 שאלות.
    """
    if q_num > 25:
        return
    
    if q_num not in st.session_state.exam_data:
        # כאן קוראים למנוע הייצור עם הפרומפט המחמיר
        new_q = generate_question_from_engine(q_num)
        st.session_state.exam_data[q_num] = new_q

def get_remaining_seconds():
    """חישוב זמן נותר מתוך 90 דקות"""
    elapsed = time.time() - st.session_state.start_time
    remaining = (90 * 60) - elapsed
    return max(0, int(remaining))

# סוף קובץ
