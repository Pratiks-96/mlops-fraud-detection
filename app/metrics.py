from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Counter: Total requests
PREDICTION_REQUESTS = Counter(
    "fraud_prediction_requests_total",
    "Total fraud prediction requests"
)

# Counter: Fraud predictions
FRAUD_PREDICTIONS = Counter(
    "fraud_predictions_total",
    "Total fraud predictions"
)

# Histogram: Latency
PREDICTION_LATENCY = Histogram(
    "fraud_prediction_latency_seconds",
    "Prediction latency in seconds"
)

# Gauge: Model health
MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Model loaded status"
)

MODEL_LOADED.set(1)


# This function exposes metrics
def get_metrics():
    return generate_latest()
