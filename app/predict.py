import numpy as np
from app.model_loader import model


def predict_fraud(request):

    data = np.array([[
        request.amount,
        request.oldbalanceOrg,
        request.newbalanceOrig,
        request.oldbalanceDest,
        request.newbalanceDest
    ]])

    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0][1]

    return {
        "fraud": bool(prediction),
        "probability": float(probability)
    }
