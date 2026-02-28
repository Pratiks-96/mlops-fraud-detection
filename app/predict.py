import numpy as np
import time

from app.model_loader import model
from app.metrics import prediction_counter, fraud_counter, prediction_latency


def predict_fraud(request):

    start = time.time()

    data = np.array([[
        request.amount,
        request.oldbalanceOrg,
        request.newbalanceOrig,
        request.oldbalanceDest,
        request.newbalanceDest
    ]])

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    prediction_counter.inc()

    if prediction == 1:
        fraud_counter.inc()

    latency = time.time() - start
    prediction_latency.observe(latency)

    return {
        "fraud": bool(prediction),
        "probability": float(probability)
    }
