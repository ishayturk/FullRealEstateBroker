# main.py - מזהה C-01

from flask import Flask, jsonify, render_template
import requests # לצורך משיכת המבחן מהלינק

app = Flask(__name__)

# הגדרת זמן לבדיקה: 3 דקות (180 שניות)
EXAM_TIME_LIMIT = 180 

@app.route('/get_exam_chunk')
def get_exam_chunk():
    # לוגיקה: פנייה ללינק המקור, הגרלת מועד, ושליפת 5 שאלות ראשונות
    # המידע נשמר בזיכרון הריצה בלבד
    try:
        # כאן תבוא הפנייה ללינק של 1213
        # response = requests.get('LINK_TO_1213_EXAMS')
        # logic to pick random exam and slice first 5...
        return jsonify({"status": "success", "questions": "first_5_data", "timer": EXAM_TIME_LIMIT})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# שאר הפונקציות של main.py נשמרות ללא שינוי (החלק הלימודי נפרד)
