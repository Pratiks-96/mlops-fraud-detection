from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Counters
PREDICTION_REQUESTS = Counter(
    "fraud_prediction_requests_total",
    "Total prediction requests"
)

FRAUD_PREDICTIONS = Counter(
    "fraud_predictions_total",
    "Total fraud predictions"
)

# Histogram
PREDICTION_LATENCY = Histogram(
    "fraud_prediction_latency_seconds",
    "Prediction latency"
)

# Gauge
MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Model loaded status"
)

MODEL_LOADED.set(1)


# Metrics endpoint function
def get_metrics():
    return generate_latest()
