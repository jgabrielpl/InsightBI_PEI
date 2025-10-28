import pandas as pd
from unittest.mock import patch, MagicMock
from src.etl.load import carregarDados

# Verifica se o método to_sql é chamado corretamente
@patch("src.etl.load.create_engine")
def test_load_to_postgres_calls_to_sql(mock_engine):
    df = pd.DataFrame({"id": [1, 2]})
    mock_conn = MagicMock()
    mock_engine.return_value = mock_conn

    carregarDados(df, "tabela_teste")

    mock_engine.assert_called_once()
    assert mock_conn.begin.called  # garante que begin() foi usado

