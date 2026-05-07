from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import time

app = FastAPI(
    title="AI Threat Detection Platform",
    version="1.0.0"
)

# Metrics
REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction latency"
)

# Load trained ML model
model = joblib.load("model/security_model.pkl")


# Request schema
class SecurityFeatures(BaseModel):
    data: list[float]


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Threat Detection Platform Running"
    }


# Prediction endpoint
@app.post("/predict")
def predict(features: SecurityFeatures):

    REQUEST_COUNT.inc()

    start_time = time.time()

    input_data = np.array(features.data).reshape(1, -1)

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0]

    confidence = round(max(probability) * 100, 2)

    risk_level = "LOW"

    if confidence > 85:
        risk_level = "HIGH"
    elif confidence > 60:
        risk_level = "MEDIUM"

    latency = time.time() - start_time

    PREDICTION_LATENCY.observe(latency)

    return {
        "threat_prediction": int(prediction),
        "confidence": confidence,
        "risk_level": risk_level
    }


# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )