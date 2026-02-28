from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import start_http_server
import time

from app.metrics import (
    PREDICTION_REQUESTS,
    FRAUD_PREDICTIONS,
    PREDICTION_LATENCY,
    MODEL_LOADED
)

app = FastAPI()

MODEL_LOADED.set(1)

def predict(amount):
    if amount > 50000:
        return 1
    return 0


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <h2>Fraud Detection</h2>
            <form action="/predict" method="post">
                Amount: <input name="amount">
                <input type="submit">
            </form>
        </body>
    </html>
    """


@app.post("/predict", response_class=HTMLResponse)
async def predict_route(amount: float = Form(...)):

    PREDICTION_REQUESTS.inc()

    start = time.time()

    result = predict(amount)

    latency = time.time() - start
    PREDICTION_LATENCY.observe(latency)

    if result == 1:
        FRAUD_PREDICTIONS.inc()

    label = "Fraud" if result == 1 else "Normal"

    return f"""
    <html>
        <body>
            <h3>Amount: {amount}</h3>
            <h3>Result: {label}</h3>
            <a href="/">Back</a>
        </body>
    </html>
    """


@app.get("/metrics")
async def metrics():
    return generate_latest()
