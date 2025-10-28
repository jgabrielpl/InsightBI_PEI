import pytest
import pandas as pd
from src.etl.extract import extrairDados

# Verificando se esta extraindo corretamente
def test_extract(tmp_path):
    test_path = tmp_path / "dados_teste.csv"
    df = pd.DataFrame({"id": [1, 2], "nome": ["Bruno", "Ana"]})
    df.to_csv(test_path, index=False)

    result = extrairDados(test_path)

    assert isinstance (result, pd.DataFrame)
    assert len(result) == 2


# Verificando se lança erro caso não achar o arquivo CSV 
def test_extract_filenotfound():
    with pytest.raises(FileNotFoundError):
        extrairDados("data/inexistente.csv")

