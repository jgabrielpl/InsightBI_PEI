import pandas as pd
import os
from src.utils.logger import getLogger

logger = getLogger()

def extrairDados(path="data/raw/dados_alunos.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo .csv não encontrado")
    
    df = pd.read_csv(path)
    logger.info(f"Dados de alunos extraidos com {len(df)} registros")
    return df

