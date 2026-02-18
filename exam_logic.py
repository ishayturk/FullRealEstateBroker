import pandas as pd
import random

def fetch_exam_data(url):
    # משיכת כל הנתונים מהמקור פעם אחת לסשן
    return pd.read_csv(url)

def initialize_exam(df, finished_exams):
    # הגרלת מועד שלא בוצע
    available_exams = [col for col in df.columns if col not in ['שאלה', 'תשובה_נכונה'] and col not in finished_exams]
    if not available_exams:
        return None, None
    
    selected_exam_col = random.choice(available_exams)
    return selected_exam_col, df[['שאלה', selected_exam_col]].copy()

def get_questions_batch(df, start_idx, end_idx):
    # טעינה מדורגת של שאלות
    return df.iloc[start_idx:end_idx]
