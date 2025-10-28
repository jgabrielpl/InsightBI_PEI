import os
import time
import requests
from src.utils.logger import getLogger
from dotenv import load_dotenv

logger = getLogger()

DISTANCE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"

def load_api_key() -> str:
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.critical("Chave da API do Google não encontrada!")
    else:
        logger.info("Chave da API do Google carregada com sucesso.")
    return api_key


def calcular_distancia(origem: str, destino: str) -> float:
    api_key = load_api_key()
    if not api_key:
        return None

    params = {
        "origins": origem,
        "destinations": destino,
        "key": api_key,
        "mode": "driving",
        "units": "metric",
        "language": "pt-BR"
    }


    for attempt in range(3):
        try:
            response = requests.get(DISTANCE_URL, params=params, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get("status") == "OK":
                element = data["rows"][0]["elements"][0]
                if element["status"] == "OK":
                    distance_m = element["distance"]["value"]
                    distance_km = round(distance_m / 1000, 2)
                    logger.info(f"Distância calculada: {distance_km} km")
                    return distance_km
                else:
                    logger.warning(f"Elemento inválido: {element['status']}")
            else:
                logger.warning(f"Tentativa {attempt+1}: erro {data.get('status')}.")
        except Exception as e:
            logger.error(f"Erro na chamada da API ({attempt+1}ª tentativa): {e}")
        time.sleep(2 ** attempt)

    logger.error("Falha após múltiplas tentativas com a API do Google Maps.")
    return None
