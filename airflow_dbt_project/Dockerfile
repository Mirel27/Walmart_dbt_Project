FROM apache/airflow:3.2.0-python3.12

USER root

RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt .

RUN python -m pip install --no-cache-dir \
    "apache-airflow==3.2.0" \
    "psycopg[binary]" \
    -r requirements.txt

RUN python -c "import psycopg; print(psycopg.__version__)"

RUN dbt --version

RUN python -m pip check