from prometheus_client import Counter, Histogram, Gauge

# total predictions
prediction_counter = Counter(
    "fraud_predictions_total",
    "Total number of predictions"
)

# fraud predictions
fraud_counter = Counter(
    "fraud_detected_total",
    "Total fraud predictions"
)

# prediction latency
prediction_latency = Histogram(
    "prediction_latency_seconds",
    "Prediction latency"
)

# app health
app_health = Gauge(
    "app_health_status",
    "Application health status"
)

app_health.set(1)
