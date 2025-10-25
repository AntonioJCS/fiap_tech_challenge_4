from __future__ import annotations

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler
try:
    from pythonjsonlogger import json
    JsonFormatter = json.JsonFormatter
except ImportError:
    from pythonjsonlogger import jsonlogger
    JsonFormatter = jsonlogger.JsonFormatter


from ftc4.common.config import settings

# Nível padrão (pode sobrescrever por env/config)
DEFAULT_LOG_LEVEL = logging.INFO

class _RequestContextFilter(logging.Filter):
    """
    Injeta 'request_id' no LogRecord a partir de um ContextVar (se existir).
    - Se você tiver um módulo ftc4.common.request_context com get_request_id(), pegamos de lá.
    - Caso não exista, seguimos com '-' (seguro).
    """
    def __init__(self, attr_name: str = "request_id"):
        super().__init__()
        self.attr_name = attr_name
        # Resolução tardia para não criar dependência rígida
        try:
            from ftc4.common.request_context import get_request_id  # type: ignore
            self._get_request_id = get_request_id  # callable
        except Exception:
            self._get_request_id = lambda: "-"

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, self.attr_name):
            try:
                setattr(record, self.attr_name, self._get_request_id())
            except Exception:
                setattr(record, self.attr_name, "-")
        return True


def _ensure_log_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger com:
      - Console bonito (RichHandler).
      - Arquivo texto clássico (app.log).
      - Arquivo JSON por linha (app.jsonl) para análise estruturada.
    Evita handlers duplicados.
    """
    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)

    if logger.handlers:
        return logger  # já configurado

    # --- Filtro de contexto (request_id) disponível para TODOS os handlers ---
    context_filter = _RequestContextFilter()

    # -------------------------
    # 1) Console (RichHandler)
    # -------------------------
    rich_handler = RichHandler(
        show_time=True,
        show_level=True,
        show_path=False,
        markup=False,               # evita precisar escapar colchetes; ligue se você usa [bold]
        rich_tracebacks=True,
        tracebacks_show_locals=True # depuração top: mostra variáveis locais no stack
    )
    # Formato simples: Rich cuida do resto
    rich_handler.setFormatter(logging.Formatter("%(name)s: %(message)s"))
    rich_handler.addFilter(context_filter)
    logger.addHandler(rich_handler)

    # --------------------------------------
    # 2) Arquivo texto clássico (app.log)
    # --------------------------------------
    try:
        log_text_path = settings.LOG_DIR / "app.log"
        _ensure_log_dir(log_text_path)
        file_handler = logging.FileHandler(log_text_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s "
            "[rid=%(request_id)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        file_handler.addFilter(context_filter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Atenção: Não foi possível configurar o FileHandler texto: {e}")

    # ---------------------------------------------------
    # 3) Arquivo estruturado JSON (app.jsonl por linha)
    # ---------------------------------------------------
    try:
        log_json_path = settings.LOG_DIR / "app.jsonl"
        _ensure_log_dir(log_json_path)
        json_handler = logging.FileHandler(log_json_path, encoding="utf-8")
        json_handler.setLevel(logging.INFO)

        # Campos padrão + quaisquer 'extra' que você passar nos .info(..., extra={...})
        json_formatter = JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
            json_indent=None,  # uma linha por evento (ideal p/ ingestão)
        )
        json_handler.setFormatter(json_formatter)
        json_handler.addFilter(context_filter)
        logger.addHandler(json_handler)
    except Exception as e:
        logger.warning(f"Atenção: Não foi possível configurar o FileHandler JSON: {e}")

    # ----------------------------------------------------
    # 4) Harmonizar níveis de uvicorn/fastapi (se quiser)
    # ----------------------------------------------------
    for name_ in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name_).setLevel(logging.INFO)

    return logger
