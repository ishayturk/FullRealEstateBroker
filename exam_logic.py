# Version: C-03
# Based on Anchor: 1218-G2
# Filename: exam_logic.py

import pandas as pd
import random

def get_unique_exam(df, finished_exams):
    all_exams = [col for col in df.columns if col not in ['שאלה', 'תשובה_נכונה']]
    available = [e for e in all_exams if e not in finished_exams]
    return random.choice(available) if available else None

def prepare_question_data(df, exam_col, start_idx, end_idx):
    actual_end = min(end_idx, 25)
    batch = df.iloc[start_idx:actual_end][['שאלה', exam_col, 'תשובה_נכונה']]
    return batch.to_dict('records')
