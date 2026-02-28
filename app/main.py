from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import time
import random

from app.metrics import (
    PREDICTION_REQUESTS,
    FRAUD_PREDICTIONS,
    PREDICTION_LATENCY,
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

history = []


# Example fraud logic (replace with real model)
def predict_fraud(amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest):

    risk = 0

    if amount > 50000:
        risk += 0.4

    if oldbalanceOrg - newbalanceOrig != amount:
        risk += 0.3

    if newbalanceDest > oldbalanceDest + amount:
        risk += 0.3

    probability = min(risk, 0.99)

    fraud = probability > 0.5

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

    data = {
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "result": result,
        "probability": round(probability * 100, 2)
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
