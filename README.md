# Fraud Detection MLOps Microservice with Prometheus & Grafana Monitoring

## Overview

This project is a **production-ready MLOps microservice** that provides real-time fraud prediction based on input values. The system supports:

* Model training using updated CSV datasets
* REST API for real-time predictions
* Kubernetes deployment for scalability
* Prometheus monitoring for metrics collection
* Grafana dashboards for visualization
* Full observability of model performance and health

This architecture follows **DevOps and MLOps best practices** for monitoring, scalability, and reliability.

---

## Architecture

```
                ┌──────────────┐
                │   Client     │
                │ (API Call)   │
                └──────┬───────┘
                       │
                       ▼
              ┌──────────────────┐
              │ ML Prediction API│
              │ (FastAPI/Flask) │
              └──────┬──────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ML Model     Prometheus     CSV Dataset
 (Trained)      Metrics        (Training)

        ▼
   Grafana Dashboard
   (Visualization)
```

---

## Features

* Real-time fraud prediction via REST API
* Model training using CSV dataset
* Automatic metrics exposure for monitoring
* Prometheus integration
* Grafana dashboard visualization
* Kubernetes-ready deployment
* Production-ready observability

---

## Tech Stack

* Python
* FastAPI / Flask
* Scikit-learn
* Docker
* Kubernetes
* Prometheus
* Grafana

---

## Project Structure

```
mlops-fraud-detection/
│
├── app/
│   ├── main.py              # Prediction API
│   ├── model.py             # Model loading
│   ├── train.py             # Model training script
│   ├── metrics.py           # Prometheus metrics
│
├── data/
│   └── fraud_data.csv       # Training dataset
│
├── model/
│   └── fraud_model.pkl      # Trained model
│
├── Dockerfile
├── requirements.txt
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
│
└── README.md
```

---

## Model Training

When the CSV file is updated, retrain the model:

```bash
python train.py
```

This will:

* Load CSV dataset
* Train ML model
* Save model as:

```
model/fraud_model.pkl
```

---

## Running the Microservice Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run API:

```bash
python main.py
```

API will run at:

```
http://localhost:8000
```

---

## Prediction API

### Endpoint

```
POST /predict
```

### Example Request

```json
{
  "feature1": 100,
  "feature2": 200,
  "feature3": 300
}
```

### Example Response

```json
{
  "prediction": 1
}
```

---

## Prometheus Metrics Endpoint

```
GET /metrics
```

Example metrics exposed:

```
fraud_prediction_requests_total
fraud_predictions_total
fraud_prediction_latency_seconds
fraud_model_loaded
```

---

## Kubernetes Deployment

Apply manifests:

```bash
kubectl apply -f kubernetes/
```

Verify pods:

```bash
kubectl get pods
```

---

## Prometheus Configuration

If Prometheus is running in the same Kubernetes cluster, use:

```
http://prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090
```

---

## Grafana Dashboard Setup

### Step 1 — Add Prometheus Data Source

Go to:

```
Grafana → Connections → Data Sources → Prometheus
```

URL:

```
http://prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090
```

Click:

```
Save & Test
```

---

### Step 2 — Import Dashboard

Go to:

```
Dashboards → Import
```

Select:

```
Import via JSON
```
updated the json file in github repo with name  grafana-dashboard.json
.

Click:

```
Load → Import
```

---

## Dashboard Metrics

The dashboard shows:

* Total Prediction Requests
* Fraud Predictions
* Fraud Rate %
* Model Health Status
* Prediction Requests per second
* Fraud Detection rate
* Prediction latency (95th percentile)

<img width="1347" height="677" alt="image" src="https://github.com/user-attachments/assets/8d748350-5847-4eff-bb86-d331c002b354" />

<img width="1346" height="673" alt="image" src="https://github.com/user-attachments/assets/b0e84589-13f8-4fcc-bb03-16e5980ca9b5" />

---

## Monitoring Example

You can monitor:

* API usage
* Model performance
* Prediction latency
* Fraud detection trends
* System health

---

## Retraining Workflow

When dataset updates:

```
Update CSV → Run train.py → Deploy new model → Monitor in Grafana
```

---

## Production Deployment Flow

```
Developer → Update Dataset
         → Train Model
         → Build Docker Image
         → Deploy to Kubernetes
         → Prometheus collects metrics
         → Grafana visualizes metrics
```

---

## Screenshots

Dashboard Example:

* Prediction metrics
* Fraud rate visualization
* Model health monitoring

<img width="1355" height="678" alt="image" src="https://github.com/user-attachments/assets/ff58acc0-f242-4a0d-a2e2-938665f50ff6" />
<img width="1343" height="678" alt="image" src="https://github.com/user-attachments/assets/268fe9db-023d-4d0d-8066-f51dcdba946a" />
<img width="1354" height="668" alt="image" src="https://github.com/user-attachments/assets/059d31ab-882f-4587-8648-86ac48c0d282" />



---

## Future Improvements

* CI/CD pipeline integration
* Automated retraining pipeline
* Model versioning
* Alertmanager integration
* Canary deployments

---

## Author

pratik
DevOps | MLOps Engineer

---

## Summary

This project demonstrates a complete **production-grade MLOps microservice** with:

* Model training
* Real-time prediction
* Kubernetes deployment
* Prometheus monitoring
* Grafana visualization
* Full observability

This setup is suitable for real-world enterprise deployment.
