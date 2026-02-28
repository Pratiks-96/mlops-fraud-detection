from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Total prediction requests
PREDICTION_REQUESTS = Counter(
    "fraud_prediction_requests_total",
    "Total fraud prediction requests"
)

# Fraud detected counter
FRAUD_PREDICTIONS = Counter(
    "fraud_predictions_total",
    "Total fraud predictions"
)

# Prediction latency
PREDICTION_LATENCY = Histogram(
    "fraud_prediction_latency_seconds",
    "Prediction latency in seconds"
)

# Model health status
MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Model loaded status (1=loaded, 0=not loaded)"
)


# Function to expose metrics endpoint
def metrics_endpoint():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
