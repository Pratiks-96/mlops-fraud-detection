FROM python:3.10

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt update && apt install -y curl

CMD ["python", "app.py"]
