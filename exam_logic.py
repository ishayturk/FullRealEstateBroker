# Version: C-04
# ID: C-01
# Description: Logic for unique exam selection and sequential question loading.

import pandas as pd
import random

def get_unique_exam(df, finished_exams):
    """מגריל מועד בחינה שטרם בוצע בסשן הנוכחי למניעת כפילות"""
    all_exams = [col for col in df.columns if col not in ['שאלה', 'תשובה_נכונה']]
    available = [e for e in all_exams if e not in finished_exams]
    if not available:
        return None
    return random.choice(available)

def prepare_question_data(df, exam_col, start_idx, end_idx):
    """שולף טווח שאלות ספציפי לצורך טעינה חסכונית (Lazy Loading)"""
    actual_end = min(end_idx, 25)
    # שליפת השאלה, עמודת המבחן הספציפי והתשובה הנכונה לצורך השוואה
    batch = df.iloc[start_idx:actual_end][['שאלה', exam_col, 'תשובה_נכונה']]
    return batch.to_dict('records')
