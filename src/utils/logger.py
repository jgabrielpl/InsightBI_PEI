import logging
import os

# Configurando o logger do projeto e salvando como Processo.log na pasta logs
def getLogger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:  # evitando duplicação
        os.makedirs("logs", exist_ok=True)
        fh = logging.FileHandler("logs/Processo.log", mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(fh)

    return logger

