# src/common/logger.py

import logging
import sys
from common.config import PROJECT_ROOT_DIR

# Caminho para o diretório de logs (relativo ao root do projeto)
LOG_DIR = PROJECT_ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Handler para terminal
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler.setFormatter(stream_format)
        logger.addHandler(stream_handler)

        # Handler para arquivo
        file_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
        file_format = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)

    return logger
