import pandas as pd
import numpy as np
import unicodedata
from src.utils.logger import getLogger

logger = getLogger()

# Remove acentos, cedilha e espaços extras de uma string
def remover_acentos(texto):
    if not isinstance(texto, str):
        return texto

    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = texto.replace("ç", "c").replace("Ç", "C")

    return texto.strip()


def transformarDados(df: pd.DataFrame):
    
    df = df.copy()
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce")
    df["data_ingresso"] = pd.to_datetime(df["data_ingresso"], errors="coerce")

    # Criando coluna de idade com data de nascimento
    data_hoje = pd.Timestamp.now().normalize()
    df["idade"] = df["data_nascimento"].apply(
        lambda d: int ((data_hoje - d).days // 365) if pd.notnull(d) else np.nan
    )

    # Garantir padronização dos valores "Sim" e "Não"
    colunas_textos = ["trancamento", "fies", "bolsas_auxilio", "negociacao_divida", "evadido"]
    for col in colunas_textos:
        if col in df.columns:
            df[col] = df[col].astype(str).str.capitalize()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].map(remover_acentos)

    logger.info("Dados transformados com sucesso")

    return df

