# FILE-ID: C-01
# VERSION-ANCHOR: 1218-G2

import time

class ExamLogic:
    def __init__(self):
        self.total_seconds = 7200
        
    def get_time_string(self, seconds_left):
        hours, remainder = divmod(seconds_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def is_question_answered(self, question_id, answers_dict):
        return question_id in answers_dict
