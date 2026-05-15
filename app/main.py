from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
import json

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import joblib
import numpy as np

from prometheus_fastapi_instrumentator import Instrumentator

from app.auth import (
    authenticate_user,
    create_access_token,
    verify_token
)

app = FastAPI(
    title="AI Threat Detection Platform",
    description="Cloud-native API for AI-assisted cybersecurity threat detection.",
    version="1.0.0"
)

Instrumentator().instrument(app).expose(app)

MODEL_METADATA_PATH = Path("model/model_metadata.json")
MODEL_METADATA = json.loads(MODEL_METADATA_PATH.read_text()) if MODEL_METADATA_PATH.exists() else {}
MODEL_PATH = Path(MODEL_METADATA.get("artifact_path", "model/security_model.pkl"))
MODEL_VERSION = MODEL_METADATA.get("model_version", "security-random-forest-v1")

if not MODEL_PATH.exists():
    raise RuntimeError(f"Model artifact not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
MODEL_FEATURE_COUNT = int(getattr(model, "n_features_in_", 0))
ALERTS = []

class PredictionRequest(BaseModel):
    data: list[float]

class ThreatExplanationRequest(BaseModel):
    prediction: int
    risk_level: str
    confidence: float | None = None

@app.get("/")
def home():
    return {
        "message": "AI Threat Detection Platform Running",
        "docs_url": "/docs",
        "health_url": "/health"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_version": MODEL_VERSION,
        "expected_features": MODEL_FEATURE_COUNT
    }

@app.get("/model-info")
def model_info():
    return {
        "model_name": MODEL_METADATA.get("model_name", "UNSW-NB15 Random Forest Threat Classifier"),
        "model_version": MODEL_VERSION,
        "model_type": MODEL_METADATA.get("model_type", type(model).__name__),
        "artifact_path": str(MODEL_PATH),
        "expected_features": MODEL_FEATURE_COUNT,
        "dataset": MODEL_METADATA.get("dataset"),
        "labels": MODEL_METADATA.get("labels", {
            "0": "normal_activity",
            "1": "threat_detected"
        }),
        "baseline_metrics": MODEL_METADATA.get("baseline_metrics"),
        "notes": MODEL_METADATA.get("notes")
    }

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/predict")
def predict(
    request: PredictionRequest,
    username: str = Depends(verify_token)
):

    try:
        if MODEL_FEATURE_COUNT and len(request.data) != MODEL_FEATURE_COUNT:
            raise HTTPException(
                status_code=400,
                detail=f"Expected {MODEL_FEATURE_COUNT} features, received {len(request.data)}"
            )

        input_data = np.array(request.data).reshape(1, -1)
        prediction = int(model.predict(input_data)[0])
        confidence = None

        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(input_data)[0]
            confidence = round(float(max(probability)), 4)

        risk_level = "HIGH" if prediction == 1 else "LOW"
        threat_status = "threat_detected" if prediction == 1 else "normal_activity"
        alert = {
            "alert_id": str(uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "prediction": prediction,
            "threat_status": threat_status,
            "risk_level": risk_level,
            "confidence": confidence,
            "model_version": MODEL_VERSION,
            "requested_by": username
        }

        ALERTS.append(alert)

        return {
            **alert,
            "recommendation": get_recommendation(risk_level)
        }

    except HTTPException:
        raise
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/alerts")
def list_alerts(username: str = Depends(verify_token)):
    return {
        "alerts": ALERTS,
        "total": len(ALERTS),
        "requested_by": username
    }

@app.post("/explain-threat")
def explain_threat(
    request: ThreatExplanationRequest,
    username: str = Depends(verify_token)
):
    status = "threat" if request.prediction == 1 else "normal network activity"
    confidence_text = (
        f"{round(request.confidence * 100, 2)}%"
        if request.confidence is not None
        else "not available"
    )

    return {
        "summary": f"The model classified this event as {status}.",
        "risk_level": request.risk_level,
        "confidence": confidence_text,
        "analyst_guidance": get_recommendation(request.risk_level),
        "requested_by": username
    }

def get_recommendation(risk_level: str):
    if risk_level.upper() == "HIGH":
        return "Review the source host, destination service, authentication activity, and recent privilege changes."

    return "No immediate action required. Continue monitoring for repeated or correlated activity."
