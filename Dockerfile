FROM apache/airflow:2.10.3-python3.11

USER airflow

WORKDIR /opt/airflow

COPY --chown=airflow:root requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root src/ /opt/airflow/src/

CMD ["bash", "-c", "airflow db upgrade && airflow users create --username ${AIRFLOW_USER} --password ${AIRFLOW_PASSWORD} --firstname Admin --lastname User --role Admin --email admin@example.com || true && airflow webserver & airflow scheduler"]
