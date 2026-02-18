# Version: C-01 (Original Logic)
import pandas as pd

def prepare_question_data(df, start_idx, end_idx):
    """טעינה חסכונית של טווח שאלות מתוך הקובץ"""
    batch = df.iloc[start_idx:min(end_idx, 25)]
    return batch.to_dict('records')
