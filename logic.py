# Project: מתווך בקליק - מערכת בחינות | File: logic.py
# Version: V209 | Date: 24/02/2026 | 00:10
import streamlit as st
import time
import random

def generate_question_from_engine(q_num):
    """
    מנוע ייצור השאלות. 
    בשלב זה, המנוע מייצר שאלות דינמיות מתוך מאגר המבוסס על חומרי הלימוד (דיני מתווכים ואתיקה).
    הפרומפט הקשיח: סיפור מקרה ארוך, שפה משפטית, 4 תשובות, נימוק מלא בתשובה הנכונה.
    """
    
    # מאגר נושאים לסימולציה (מבוסס על הלינקים שסיפקת: חוק המתווכים, אתיקה, מקרקעין)
    pool = [
        {
            "topic": "דמי תיווך וגורם יעיל",
            "q": "מתווך הראה דירה ללקוח. לאחר חודשיים הלקוח רכש את הדירה ישירות מהבעלים מבלי לערב את המתווך, בטענה שהמתווך רק 'פתח את הדלת' ולא עשה דבר מעבר לכך. המתווך הגיש תביעה לדמי תיווך.",
            "correct": "המתווך זכאי לדמי תיווך אם יוכיח שהיה 'הגורם היעיל' שהביא להתגבשות העסקה, גם אם לא נכח במעמד החתימה, ובלבד שקיים הסכם בכתב.",
            "distractors": [
                "המתווך אינו זכאי לדמי תיווך בשום מקרה אם לא נכח במו\"מ הסופי.",
                "הלקוח תמיד פטור מדמי תיווך אם עברו יותר מ-30 יום מהצגת הנכס.",
                "המתווך זכאי רק ל-50% מהעמלה כי הוא לא ניהל את המו\"מ."
            ]
        },
        {
            "topic": "אתיקה וגילוי נאות",
            "q": "מתווך מייצג מוכר דירה. במהלך המו\"מ נודע למתווך כי בכוונת העירייה להקים אתר פסולת במרחק 200 מטר מהנכס בעוד כשנתיים. המוכר ביקש מהמתווך לא לגלות זאת לקונים פוטנציאליים כדי לא להוריד את המחיר.",
            "correct": "על המתווך חובה חוקית לגלות לקונה כל מידע מהותי הנוגע לנכס, וחובה זו גוברת על הוראת המוכר להסתיר מידע.",
            "distractors": [
                "המתווך חייב לפעול בנאמנות למוכר בלבד ולכן אסור לו לגלות את המידע ללא אישורו.",
                "המתווך רשאי לשתוק, שכן זוהי חובתו של הקונה לבצע בדיקות בעירייה.",
                "החובה חלה רק אם המתווך נשאל על כך ישירות על ידי הקונה."
            ]
        },
        {
            "topic": "בלעדיות ותקופות",
            "q": "לקוח חתם על הסכם בלעדיות למכירת חנות למשך תקופה של שנה אחת. המתווך ביצע את פעולות השיווק הנדרשות. החנות נמכרה לאחר 10 חודשים דרך מתווך אחר.",
            "correct": "הבלעדיות פקעה; לפי חוק המתווכים, תקופת הבלעדיות המקסימלית בנכס שאינו דירת מגורים היא שנה, אך בדירת מגורים היא 6 חודשים.",
            "distractors": [
                "המתווך זכאי לדמי תיווך מלאים כי שנה היא התקופה החוקית לכל סוגי הנכסים.",
                "הסכם הבלעדיות בטל מעיקרו כי אסור להחתים על יותר מ-3 חודשים.",
                "המתווך זכאי רק להחזר הוצאות שיווק ללא עמלה."
            ]
        }
    ]
    
    # בחירת שאלה מהמאגר (או ייצור לפי סדר למניעת חזרתיות)
    data = pool[(q_num - 1) % len(pool)]
    
    options = [data["correct"]] + data["distractors"]
    random.shuffle(options)
    ans_idx = options.index(data["correct"])
    
    return {
        "question": data["q"],
        "options": options,
        "answer_index": ans_idx
    }

def initialize_exam_state():
    if "exam_data" not in st.session_state:
        st.session_state.exam_data = {}
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
    if q_num > 25:
        return
    if q_num not in st.session_state.exam_data:
        st.session_state.exam_data[q_num] = generate_question_from_engine(q_num)

def get_remaining_seconds():
    elapsed = time.time() - st.session_state.start_time
    remaining = (90 * 60) - elapsed
    return max(0, int(remaining))

# סוף קובץ
