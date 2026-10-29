FROM apache/airflow:3.3.2-python3.10

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential openjdk-17-jre-headless curl libkrb5-dev \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir \
      --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.10.txt \
      -r /requirements.txt

WORKDIR /opt/airflow
