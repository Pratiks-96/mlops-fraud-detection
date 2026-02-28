from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.schema import FraudRequest
from app.predict import predict_fraud

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(request: FraudRequest):

    result = predict_fraud(request)

    return result
