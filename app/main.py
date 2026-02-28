from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time
import random

from app.metrics import (
    PREDICTION_REQUESTS,
    FRAUD_PREDICTIONS,
    PREDICTION_LATENCY,
)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# store prediction history
history = []

def predict(amount):
    probability = min(amount / 100000, 1.0)
    result = 1 if probability > 0.5 else 0
    return result, probability


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "history": history,
            "result": None,
        },
    )


@app.post("/predict", response_class=HTMLResponse)
async def predict_route(request: Request, amount: float = Form(...)):

    PREDICTION_REQUESTS.inc()

    start = time.time()

    result, probability = predict(amount)

    latency = time.time() - start
    PREDICTION_LATENCY.observe(latency)

    if result == 1:
        FRAUD_PREDICTIONS.inc()

    label = "Fraud" if result else "Normal"

    # store history
    history.append({
        "amount": amount,
        "result": label,
        "probability": round(probability * 100, 2)
    })

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "history": history,
            "result": label,
            "probability": round(probability * 100, 2),
        },
    )
