FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install  --assume-yes --no-install-recommends --no-install-suggests \
    build-essential \
    curl \
    gcc \
    kafkacat \
    librdkafka-dev \
    librdkafka1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "sniffer_app.py"]

CMD ["python3", "-u", "/app/main.py"]