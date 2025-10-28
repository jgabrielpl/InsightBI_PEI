from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os

from src.etl.extract import extrairDados
from src.etl.transform import transformarDados
from src.etl.load import carregarDados
from src.etl.enrichment import rodarGoogleAPI
from src.utils.logger import getLogger

logger = getLogger()

default_args = {
    'owner': 'evasaopei_team', 
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="etl_faculdade_dag",
    description="Pipeline ETL de dados de alunos da faculdade",
    default_args=default_args,
    start_date=datetime(2025, 10, 27),
    catchup=False,
    tags=["evasaoPEI"],
) as dag:
    
    def taskExtrair(**kwargs):
        logger.info("Iniciando extração...")
        df = extrairDados(path = "data/raw/dados_alunos.csv")
        os.makedirs("data/tmp", exist_ok=True)
        df.to_parquet("data/tmp/extracted.parquet", index=False)
        logger.info(f"Extração feita com sucesso, com {len(df)} registros.")
    
    
    def taskTransformar(**kwargs):
        logger.info("Iniciando transformação...")

        df = pd.read_parquet("data/tmp/extracted.parquet")
        df_transformed = transformarDados(df)
        df_transformed.to_parquet("data/tmp/transformed.parquet", index=False)
        logger.info(f"Transformação feita com sucesso, com {df_transformed.shape[0]} registros.")


    def taskEnriquecimento(**kwargs):
        logger.info("Iniciando enriquecimento com google maps api...")
        df = pd.read_parquet("data/tmp/transformed.parquet")
        df_enriched = rodarGoogleAPI(df)
        df_enriched.to_parquet("data/tmp/enriched.parquet", index=False)
        logger.info("Enriquecimento feito com sucesso, com coluna de distância adicionada.")

    
    def taskCarregar(**kwargs):
        logger.info("Iniciando o load...")
        df = pd.read_parquet("data/tmp/enriched.parquet")
        carregarDados(df)
        logger.info("Carregamento feito com sucesso")



    extrair = PythonOperator(
        task_id= 'extrair_dados',
        python_callable= taskExtrair,
        provide_context= True
    )

    transformar = PythonOperator(
        task_id="transformar_dados",
        python_callable=taskTransformar
    )

    enriquecer = PythonOperator(
    task_id="enriquecer_dados", 
    python_callable=taskEnriquecimento
    )

    carregar = PythonOperator(
        task_id="carregar_dados", 
        python_callable=taskCarregar
    )

    extrair >> transformar >> enriquecer >> carregar
