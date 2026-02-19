from flask import Flask, render_template, redirect, url_for
from logic import ExamLogic

app = Flask(__name__)

# טעינת המבחן מהתיקייה exams_data לפי הפורמט שקבענו
# לצורך הדוגמה נשתמש ב-test_may1_v1_2025.json
exam = ExamLogic("exams_data/test_may1_v1_2025.json")

@app.route('/')
def index():
    # שליפת השאלה הנוכחית בלבד לפי האינדקס בלוגיקה
    current_question = exam.get_current_question()
    
    if not current_question:
        return "הבחינה הסתיימה"
    
    return render_template('index.html', 
                           question=current_question, 
                           index=exam.current_index + 1,
                           total=len(exam.questions))

@app.route('/next')
def next_question():
    exam.next_question()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
