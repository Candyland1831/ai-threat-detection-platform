from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time

app = FastAPI()

REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction latency"
)

@app.post("/predict")
def predict(data: dict):

    REQUEST_COUNT.inc()   # <-- THIS increases the counter

    start_time = time.time()

    # fake prediction
    result = {"prediction": "approved"}

    latency = time.time() - start_time
    PREDICTION_LATENCY.observe(latency)

    return result


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")