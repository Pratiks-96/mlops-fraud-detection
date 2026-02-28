from fastapi import FastAPI
from app.schema import FraudRequest
from app.predict import predict_fraud

app = FastAPI(title="Fraud Detection API")


@app.get("/")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: FraudRequest):

    result = predict_fraud(request)

    return result
