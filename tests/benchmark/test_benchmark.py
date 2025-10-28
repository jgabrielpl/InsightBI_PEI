import time, os
import pytest
from unittest.mock import patch, MagicMock
from src.etl.extract import extrairDados
from src.etl.transform import transformarDados
from src.etl.enrichment import rodarGoogleAPI
from src.etl.load import carregarDados

@pytest.mark.benchmark
def test_benchmark(tmp_path, df_exemplo):
    test_path = tmp_path / "dados_teste.csv"
    df_exemplo.to_csv(test_path, index=False)

    tempos = {}

    # Extract
    start = time.perf_counter()
    df = extrairDados(test_path)
    tempos["extract"] = time.perf_counter() - start

    # Transform
    start = time.perf_counter()
    df = transformarDados(df)
    tempos["transform"] = time.perf_counter() - start

    # Enrichment
    with patch("src.etl.enrichment.calcular_distancia", return_value=3.14), patch("src.etl.enrichment.os.getenv", return_value=" "):
        start = time.perf_counter()
        df = rodarGoogleAPI(df)
        tempos["enrichment"] = time.perf_counter() - start

    # Load
    with patch("src.etl.load.create_engine") as mock_engine:
        mock_conn = MagicMock()
        mock_engine.return_value = mock_conn
        start = time.perf_counter()
        carregarDados(df, "alunos_benchmark")
        tempos["load"] = time.perf_counter() - start

    # Mostrando os resultados Benchmark
    total = sum(tempos.values())
    print("\n Benchmark Pipeline ETL (em segundos)")
    for etapa, duracao in tempos.items():
        print(f"{etapa:<12}: {duracao:.4f}s")
    print(f"Total       : {total:.4f}s")

    from datetime import datetime
    os.makedirs("logs", exist_ok=True)
    with open("logs/benchmark.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        for etapa, duracao in tempos.items():
            f.write(f"{etapa:<12}: {duracao:.4f}s\n")
        f.write(f"Total       : {total:.4f}s\n")
    
