FROM apache/airflow:3.0.0

USER root
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

ENV PATH="/home/airflow/.local/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt