This is mlops microservice it can predict the number based on the input values we updated the csv file for the building or traning the module 
<img width="1359" height="677" alt="image" src="https://github.com/user-attachments/assets/a9991101-fdc2-4182-aca7-055009bd00f8" />

Add Prometheus datasource
Connections → Data sources → Prometheus
URL:(note : if promethus running on same server or same k8s cluster then use this url :  http://prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090 )
click : Save & Test


Option 1 — Import via JSON (Recommended)
Step 1 — Click
Dashboards → Import
Import via grafana.com
Import via JSON
Upload JSON file
Import via JSON

Copy FULL JSON below and paste:

{
  "title": "Fraud Detection MLOps Dashboard",
  "timezone": "browser",
  "panels": [
    {
      "type": "stat",
      "title": "Total Prediction Requests",
      "targets": [
        {
          "expr": "fraud_prediction_requests_total"
        }
      ],
      "gridPos": { "x": 0, "y": 0, "w": 6, "h": 4 }
    },
    {
      "type": "stat",
      "title": "Fraud Predictions",
      "targets": [
        {
          "expr": "fraud_predictions_total"
        }
      ],
      "gridPos": { "x": 6, "y": 0, "w": 6, "h": 4 }
    },
    {
      "type": "stat",
      "title": "Fraud Rate %",
      "targets": [
        {
          "expr": "(fraud_predictions_total / fraud_prediction_requests_total) * 100"
        }
      ],
      "gridPos": { "x": 12, "y": 0, "w": 6, "h": 4 }
    },
    {
      "type": "stat",
      "title": "Model Health",
      "targets": [
        {
          "expr": "fraud_model_loaded"
        }
      ],
      "gridPos": { "x": 18, "y": 0, "w": 6, "h": 4 }
    },
    {
      "type": "timeseries",
      "title": "Prediction Requests/sec",
      "targets": [
        {
          "expr": "rate(fraud_prediction_requests_total[1m])"
        }
      ],
      "gridPos": { "x": 0, "y": 4, "w": 12, "h": 8 }
    },
    {
      "type": "timeseries",
      "title": "Fraud Detection/sec",
      "targets": [
        {
          "expr": "rate(fraud_predictions_total[1m])"
        }
      ],
      "gridPos": { "x": 12, "y": 4, "w": 12, "h": 8 }
    },
    {
      "type": "timeseries",
      "title": "Prediction Latency (95%)",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(fraud_prediction_latency_seconds_bucket[5m]))"
        }
      ],
      "gridPos": { "x": 0, "y": 12, "w": 24, "h": 8 }
    }
  ],
  "schemaVersion": 36,
  "version": 1,
  "refresh": "5s"
}

click : Load
<img width="1348" height="672" alt="image" src="https://github.com/user-attachments/assets/13515fc8-d23c-4396-be35-d0c55fac5026" />
<img width="1355" height="666" alt="image" src="https://github.com/user-attachments/assets/c9ff8f23-761f-4157-80d0-0236cd223c5d" />



