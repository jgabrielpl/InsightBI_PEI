import pandas as pd
from src.etl.transform import transformarDados

# Colunas devem estar em snake_case após transformação
def test_transform(df_exemplo):
    df = transformarDados(df_exemplo)
    assert all(col == col.lower() for col in df.columns)
    assert all(" " not in col for col in df.columns)
    obrigatorias = {"id", "data_nascimento", "data_ingresso", "idade"}
    assert obrigatorias.issubset(df.columns)


# Datas devem ser convertidas para datetime
def test_transform_date_columns(df_exemplo):
    df = transformarDados(df_exemplo)
    assert pd.api.types.is_datetime64_any_dtype(df["data_nascimento"])
    assert pd.api.types.is_datetime64_any_dtype(df["data_ingresso"])


# Cria coluna de idade com base na data de nascimento
def test_transform_age_column(df_exemplo):
    df = transformarDados(df_exemplo)
    assert "idade" in df.columns
    assert df["idade"].notnull().all()


# Padroniza colunas de texto com "Sim" e "Não"
def test_transform_text_columns(df_exemplo):
    df = transformarDados(df_exemplo)
    for col in ["trancamento", "fies", "bolsas_auxilio", "negociacao_divida", "evadido"]:
        assert df[col].isin(["Sim", "Não"]).all()

