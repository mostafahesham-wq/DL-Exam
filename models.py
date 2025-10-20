# backend/app/models.py
from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    Pregnancies: float = Field(..., example=2)
    Glucose: float = Field(..., example=120)
    BloodPressure: float = Field(..., example=70)
    SkinThickness: float = Field(..., example=25)
    Insulin: float = Field(..., example=100)
    BMI: float = Field(..., example=30.5)
    DiabetesPedigreeFunction: float = Field(..., example=0.5)
    Age: float = Field(..., example=35)

class PredictResponse(BaseModel):
    prediction: int
    probability: float
    class_name: str

class BatchPredictRequest(BaseModel):
    instances: List[PredictRequest]

class BatchPredictResponseItem(BaseModel):
    prediction: int
    probability: float
    class_name: str

class BatchPredictResponse(BaseModel):
    results: List[BatchPredictResponseItem]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
