from prometheus_client import Counter, Histogram, Gauge

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
    "Prediction latency"
)

# Model health
MODEL_LOADED = Gauge(
    "fraud_model_loaded",
    "Model loaded status"
)
