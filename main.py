# logic_update_1218_G2.py

def render_exam_interface(exam_data):
    # 1. הסרת הכותרות המיותרות - ניגשים ישר להוראות ולשאלות
    instructions = exam_data['exam_info'].get('instructions', "")
    
    # 2. הגדרת הטיימר בראש העמוד (ולא בסיידבר)
    # הטיימר נמשך מה-JSON (90 דקות) ומוצג כאלמנט צף עליון
    timer_html = f'<div id="timer" style="position:fixed; top:10px; right:20px; z-index:1000;"></div>'
    
    # 3. תצוגת השאלות בפריסה מלאה (Full Width)
    render_questions(exam_data['questions'])

# עדכון CSS למניעת קפיצת סיידבר
"""
#sidebar { display: none; } 
.content { width: 100%; max-width: 800px; margin: 0 auto; }
"""
