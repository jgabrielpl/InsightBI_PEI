import pytest
import pandas as pd
from unittest.mock import patch
from src.etl.enrichment import rodarGoogleAPI

# Verifica se adiciona coluna de distância corretamente.
@patch("src.etl.enrichment.calcular_distancia", return_value=3.2)
@patch("src.etl.enrichment.os.getenv", return_value=" ") 
def test_enrichment_adds_distance_column(mock_env, mock_calc, df_exemplo):
    df = rodarGoogleAPI(df_exemplo)
    assert "distancia_residencia_faculdade" in df.columns
    assert df["distancia_residencia_faculdade"].notnull().all()
    mock_calc.assert_called()


# Se ENDERECO_FACULDADE não estiver configurado, coluna deve existir com None.
@patch("src.etl.enrichment.os.getenv", return_value=None)
def test_enrichment_handles_missing_env(mock_env, df_exemplo):
    df = rodarGoogleAPI(df_exemplo)
    assert "distancia_residencia_faculdade" in df.columns
    assert df["distancia_residencia_faculdade"].isnull().all()

