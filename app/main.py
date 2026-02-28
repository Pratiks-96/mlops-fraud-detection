from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.schema import FraudRequest
from app.predict import predict_fraud

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# store prediction history
history = []


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "history": history}
    )


@app.post("/predict")
def predict(request: FraudRequest):

    result = predict_fraud(request)

    history.append(result)

    return result


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/health")
def health():
    return {"status": "healthy"}
