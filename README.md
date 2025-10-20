# Diabetes Prediction API (FastAPI)

## Structure
- `app/` : FastAPI application code
- `models/` : place `best_model.h5` and `scaler.save` here
- `requirements.txt` : Python dependencies

## Setup (Windows / macOS / Linux)
1. Create venv and activate:
   - Windows (PowerShell):
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:

3. Place the trained model and scaler:

4. Run the app:

5. Open docs:
- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/redoc` (ReDoc)

## API usage
- **Health**: `GET /health`
- **Single prediction**: `POST /predict` (JSON body) — requires header `X-API-KEY: <key>`
- **Batch prediction**: `POST /predict_batch` with `{"instances":[{...}, {...}]}` — requires API key
- **Model info**: `GET /model_info` — requires API key

Default API key: `CHANGE_ME_TO_A_RANDOM_SECRET` (in `app/auth.py`). Replace with secure value.

## Logging
- Requests are appended to `backend/request_logs.csv` with timestamp, endpoint, payload, response and status code.


