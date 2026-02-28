from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Total prediction requests
PREDICTION_REQUESTS = Counter(
    "fraud_prediction_requests_total",
    "Total number of fraud prediction requests"
)

# Fraud predictions count
FRAUD_PREDICTIONS = Counter(
    "fraud_predictions_total",
    "Total number of fraud detected predictions"
)

# Latency histogram
PREDICTION_LATENCY = Histogram(
    "fraud_prediction_latency_seconds",
    "Time spent processing prediction"
)

# Model health
MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Model loaded status (1=loaded, 0=not loaded)"
)

# Set model loaded
MODEL_LOADED.set(1)


# Metrics endpoint function
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
