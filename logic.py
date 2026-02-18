import threading
import time

class ExamLogic:
    def __init__(self, total_time_seconds=7200):
        self.total_time = total_time_seconds
        self.time_left = total_time_seconds
        self.timer_started = False
        self.is_running = True
        self.user_answers = {}
        
    def start_timer(self, update_callback):
        """
        מפעיל את הטיימר ב-Thread נפרד כדי שלא יתקע את הממשק (main.py)
        update_callback: פונקציה מהממשק שתעדכן את התצוגה בכל שנייה
        """
        if not self.timer_started:
            self.timer_started = True
            thread = threading.Thread(target=self._run_timer, args=(update_callback,), daemon=True)
            thread.start()

    def _run_timer(self, update_callback):
        while self.is_running and self.time_left > 0:
            if self.timer_started:
                time.sleep(1)
                self.time_left -= 1
                # שליחת הזמן המעודכן חזרה לממשק מבלי לתקוע אותו
                update_callback(self.time_left)
            else:
                # מחכה עד שהטיימר יופעל רשמית
                time.sleep(0.5)

    def trigger_interaction(self, update_callback):
        """נקרא מכל לחיצה ב-main.py"""
        if not self.timer_started:
            self.start_timer(update_callback)

    def stop_logic(self):
        self.is_running = False

    def get_time_string(self):
        hours, remainder = divmod(self.time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
