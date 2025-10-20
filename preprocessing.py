# backend/app/preprocessing.py
import pandas as pd
import numpy as np

# Feature order MUST match the order used during training/scaler fit
FEATURE_ORDER = [
    "Pregnancies","Glucose","BloodPressure","SkinThickness",
    "Insulin","BMI","DiabetesPedigreeFunction","Age"
]

def to_dataframe(input_dict):
    """
    Convert a dict of features (keys matching FEATURE_ORDER) to a 1xN pandas DataFrame.
    """
    # Ensure keys order and missing detection
    row = {k: input_dict.get(k, None) for k in FEATURE_ORDER}
    df = pd.DataFrame([row], columns=FEATURE_ORDER)
    return df

def batch_to_dataframe(list_of_dicts):
    rows = []
    for d in list_of_dicts:
        rows.append({k: d.get(k, None) for k in FEATURE_ORDER})
    df = pd.DataFrame(rows, columns=FEATURE_ORDER)
    return df
