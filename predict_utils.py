# backend/app/predict_utils.py
import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
# Paths relative to backend/app/ -> backend/models/
MODEL_PATH = os.path.join(os.path.dirname(BASE_DIR), "DL Exam/models", "best_model.h5")
SCALER_PATH = os.path.join(os.path.dirname(BASE_DIR), "DL Exam/models", "scaler.save")

# safe loader with messages
def load_artifacts(model_path: str = MODEL_PATH, scaler_path: str = SCALER_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found at: {scaler_path}")
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_single(model, scaler, df_row):
    """
    df_row: pandas DataFrame with shape (1, n_features) in correct order
    returns: (prediction_int, probability_float)
    """
    X = scaler.transform(df_row.values)  # use same scaler
    prob = float(model.predict(X)[0][0])
    pred = int(prob > 0.5)
    return pred, prob

def predict_batch(model, scaler, df):
    X = scaler.transform(df.values)
    probs = model.predict(X).ravel()
    preds = (probs > 0.5).astype(int)
    return preds.tolist(), probs.tolist()
