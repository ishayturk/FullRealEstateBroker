import json

class ExamLogic:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)
        self.current_index = 0

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def next_question(self):
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
