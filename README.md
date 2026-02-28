mlops-fraud-detection/
│
├── app/
│   ├── main.py
│   ├── model_loader.py
│   ├── predict.py
│
├── model/
│   └── fraud_model.pkl     ← already trained model
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│
├── .github/workflows/
│   └── ci.yml
│
├── requirements.txt
├── Dockerfile
└── .dockerignore
