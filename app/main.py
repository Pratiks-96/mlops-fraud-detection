from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.metrics import metrics_endpoint
import time

from app.metrics import (
    PREDICTION_REQUESTS,
    FRAUD_PREDICTIONS,
    PREDICTION_LATENCY,
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

history = []


# ✅ Improved fraud probability calculation
def predict_fraud(amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest):

    score = 0.0

    # Feature 1: Amount ratio risk
    if oldbalanceOrg > 0:
        amount_ratio = amount / oldbalanceOrg
        score += min(amount_ratio, 1.0) * 0.4

    # Feature 2: Origin balance mismatch risk
    expected_orig = oldbalanceOrg - amount
    orig_error = abs(expected_orig - newbalanceOrig)

    orig_error_ratio = orig_error / max(oldbalanceOrg, 1)
    score += min(orig_error_ratio, 1.0) * 0.3

    # Feature 3: Destination balance anomaly risk
    expected_dest = oldbalanceDest + amount
    dest_error = abs(expected_dest - newbalanceDest)

    dest_error_ratio = dest_error / max(amount, 1)
    score += min(dest_error_ratio, 1.0) * 0.3

    # Normalize probability
    probability = min(max(score, 0.0), 1.0)

    fraud = probability >= 0.5

    return fraud, probability


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "history": history
        }
    )


@app.post("/predict", response_class=HTMLResponse)
async def predict(

    request: Request,

    amount: float = Form(...),
    oldbalanceOrg: float = Form(...),
    newbalanceOrig: float = Form(...),
    oldbalanceDest: float = Form(...),
    newbalanceDest: float = Form(...),
):

    PREDICTION_REQUESTS.inc()

    start = time.time()

    fraud, probability = predict_fraud(
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest
    )

    latency = time.time() - start
    PREDICTION_LATENCY.observe(latency)

    if fraud:
        FRAUD_PREDICTIONS.inc()

    result = "Fraud" if fraud else "Normal"

    probability_percent = round(probability * 100, 2)

    data = {
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "result": result,
        "probability": probability_percent
    }

    history.append(data)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "history": history,
            "prediction": data
        }
    )


@app.get("/api/history")
async def get_history():
    return JSONResponse(history)


@app.get("/metrics")
async def metrics():
    return metrics_endpoint()
