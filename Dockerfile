FROM python:3.10-slim-buster AS builder

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]