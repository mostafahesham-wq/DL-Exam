# backend/app/logger.py
import csv
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "request_logs.csv")

def log_request(endpoint: str, payload: dict, response: dict, status_code: int):
    header = ["timestamp", "endpoint", "payload", "response", "status_code"]
    row = [datetime.utcnow().isoformat(), endpoint, str(payload), str(response), str(status_code)]
    exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow(row)
