# backend/main.py
import os
import traceback
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .models import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse, HealthResponse
from .preprocessing import to_dataframe, batch_to_dataframe, FEATURE_ORDER
from .predict_utils import load_artifacts, predict_single, predict_batch
from .logger import log_request
from .auth import get_api_key

# ---- App Initialization ----
app = FastAPI(title="Diabetes Prediction API", version="1.0")

# CORS (open for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Globals ----
model = None
scaler = None
model_loaded = False

# ---- Startup Event ----
@app.on_event("startup")
def startup_event():
    global model, scaler, model_loaded
    try:
        model, scaler = load_artifacts()
        model_loaded = True
        print("Loaded model and scaler.")
    except Exception as e:
        model_loaded = False
        print("Failed to load artifacts:", e)
        traceback.print_exc()

# ---- Health Endpoint ----
@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="healthy", model_loaded=bool(model_loaded))

# ---- Single Prediction ----
@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest, api_key: str = Depends(get_api_key)):
    try:
        df = to_dataframe(request.dict())
        if df.isnull().any().any():
            raise HTTPException(status_code=422, detail="Missing or invalid features in request.")
        pred, prob = predict_single(model, scaler, df)
        class_name = "Positive" if pred == 1 else "Negative"
        response = PredictResponse(prediction=pred, probability=prob, class_name=class_name)
        log_request("/predict", request.dict(), response.dict(), 200)
        return response
    except HTTPException as he:
        log_request("/predict", request.dict(), {"error": he.detail}, he.status_code)
        raise he
    except Exception as e:
        traceback.print_exc()
        log_request("/predict", request.dict(), {"error": str(e)}, 500)
        raise HTTPException(status_code=500, detail="Prediction failed.")

# ---- Batch Prediction ----
@app.post("/predict_batch", response_model=BatchPredictResponse)
def predict_batch_endpoint(req: BatchPredictRequest, api_key: str = Depends(get_api_key)):
    try:
        df = batch_to_dataframe([inst.dict() for inst in req.instances])
        if df.isnull().any().any():
            raise HTTPException(status_code=422, detail="Missing or invalid features in one or more instances.")
        preds, probs = predict_batch(model, scaler, df)
        results = []
        for p, pr in zip(preds, probs):
            results.append({"prediction": int(p), "probability": float(pr), "class_name": "Positive" if p==1 else "Negative"})
        response = BatchPredictResponse(results=results)
        log_request("/predict_batch", [i.dict() for i in req.instances], response.dict(), 200)
        return response
    except HTTPException as he:
        log_request("/predict_batch", [i.dict() for i in req.instances], {"error": he.detail}, he.status_code)
        raise he
    except Exception as e:
        traceback.print_exc()
        log_request("/predict_batch", [i.dict() for i in req.instances], {"error": str(e)}, 500)
        raise HTTPException(status_code=500, detail="Batch prediction failed.")

# ---- Serve Frontend ----
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    path = os.path.join(frontend_path, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
