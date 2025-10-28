import pandas as pd
import os
from src.utils.logger import getLogger
from dotenv import load_dotenv
from src.utils.googleapi import calcular_distancia

logger = getLogger()

def rodarGoogleAPI(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    load_dotenv(override=True)
    faculdade_endereco = os.getenv("ENDERECO_FACULDADE")

    if not faculdade_endereco:
        logger.critical("Endereço da faculdade não configurado no .env.")
        df["distancia_residencia_faculdade"] = None
        return df

    logger.info(f"Calculando distâncias até: {faculdade_endereco}")

    df["distancia_residencia_faculdade"] = df["endereco"].apply(
        lambda e: calcular_distancia(e, faculdade_endereco)
    )

    logger.info("Coluna 'distancia_residencia_faculdade' adicionada com sucesso.")
    return df

