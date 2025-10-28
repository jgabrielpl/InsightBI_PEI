import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from src.utils.logger import getLogger

load_dotenv()
logger = getLogger()

def carregarDados(df: pd.DataFrame, table_name = "alunos"):

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

    try:
        with engine.begin() as conn:
            df.to_sql(table_name, con=conn, if_exists="replace", index=False)
            logger.info(f"Dados carregados com sucesso.")
    except Exception as exc:
        logger.error(f"Erro ao carregar dados {exc}")
        raise

