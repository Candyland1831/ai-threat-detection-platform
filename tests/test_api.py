from unittest.mock import patch

from fastapi.testclient import TestClient

with patch("joblib.load") as mock_load:
    mock_model = mock_load.return_value
    mock_model.n_features_in_ = 43
    mock_model.predict.return_value = [0]
    mock_model.predict_proba.return_value = [[0.86, 0.14]]

    from app.main import app


client = TestClient(app)
SAMPLE_FEATURES = [
    1.0, 0.000011, 117.0, 0.0, 4.0, 2.0, 0.0, 496.0, 0.0,
    90909.0902, 254.0, 0.0, 180363632.0, 0.0, 0.0, 0.0, 0.011,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 248.0,
    0.0, 0.0, 0.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.0, 0.0,
    0.0, 1.0, 2.0, 0.0
]


def auth_headers():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "password123"},
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_home_endpoint_returns_platform_status():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "AI Threat Detection Platform Running"


def test_health_endpoint_reports_model_status():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["model_loaded"] is True
    assert body["model_version"] == "security-random-forest-v1"
    assert body["expected_features"] == 43


def test_model_info_returns_artifact_metadata():
    response = client.get("/model-info")

    assert response.status_code == 200
    body = response.json()
    assert body["model_version"] == "security-random-forest-v1"
    assert body["expected_features"] == 43
    assert body["labels"]["0"] == "normal_activity"


def test_login_returns_bearer_token_for_valid_user():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_rejects_invalid_credentials():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_predict_returns_security_context_and_creates_alert():
    response = client.post(
        "/predict",
        json={"data": SAMPLE_FEATURES},
        headers=auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] in [0, 1]
    assert body["threat_status"] in ["normal_activity", "threat_detected"]
    assert body["risk_level"] in ["LOW", "HIGH"]
    assert body["model_version"] == "security-random-forest-v1"
    assert body["requested_by"] == "admin"
    assert body["alert_id"]


def test_predict_rejects_wrong_feature_count():
    response = client.post(
        "/predict",
        json={"data": [1.0, 2.0, 3.0]},
        headers=auth_headers(),
    )

    assert response.status_code == 400
    assert "Expected 43 features" in response.json()["detail"]


def test_alerts_endpoint_requires_auth_and_returns_alerts():
    client.post(
        "/predict",
        json={"data": SAMPLE_FEATURES},
        headers=auth_headers(),
    )

    response = client.get("/alerts", headers=auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert body["requested_by"] == "admin"


def test_explain_threat_returns_analyst_guidance():
    response = client.post(
        "/explain-threat",
        json={"prediction": 1, "risk_level": "HIGH", "confidence": 0.91},
        headers=auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "HIGH"
    assert "classified" in body["summary"]
    assert body["requested_by"] == "admin"
