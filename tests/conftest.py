import pandas as pd
import pytest
from datetime import datetime, timedelta

@pytest.fixture

# Criando um DataFrame de exemplo, do mesmo formato que o dados_alunos.csv

def df_exemplo():
    data = {
        "id": [1, 2],
        "data_nascimento": [
            (datetime.now() - timedelta(days=365 * 20)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=365 * 25)).strftime("%Y-%m-%d"),
        ],
        "genero": ["Masculino", "Feminino"],
        "raca_etnia": ["Branca", "Parda"],
        "estado_civil": ["Solteiro", "Casado"],
        "naturalidade": ["Cuiabá-MT", "VG-MT"],
        "endereco": ["Rua A, 123", "Rua B, 456"],
        "renda_familiar": [2000, 3500],
        "trabalha_estagia": ["Sim", "Não"],
        "escola_ensino_medio": ["Pública", "Privada"],
        "escolaridade_pais": ["Médio", "Superior"],
        "meio_transporte": ["Ônibus", "Carro"],
        "curso": ["Engenharia", "Direito"],
        "turno": ["Noite", "Manhã"],
        "data_ingresso": [
            (datetime.now() - timedelta(days=365 * 2)).strftime("%Y-%m-%d"),
            (datetime.now() - timedelta(days=365 * 1)).strftime("%Y-%m-%d"),
        ],
        "forma_ingresso": ["Vestibular", "Enem"],
        "trancamento": ["sim", "não"],
        "fies": ["sim", "não"],
        "bolsas_auxilio": ["não", "sim"],
        "negociacao_divida": ["não", "sim"],
        "evadido": ["não", "sim"],
    }
    return pd.DataFrame(data)

