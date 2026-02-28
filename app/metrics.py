from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

PREDICTION_REQUESTS = Counter(
    "fraud_prediction_requests_total",
    "Total fraud prediction requests"
)

FRAUD_PREDICTIONS = Counter(
    "fraud_predictions_total",
    "Total fraud predictions"
)

PREDICTION_LATENCY = Histogram(
    "fraud_prediction_latency_seconds",
    "Prediction latency"
)

MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Model loaded status"
)

MODEL_LOADED.set(1)


def metrics_endpoint():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
