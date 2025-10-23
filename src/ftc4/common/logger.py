import logging
import sys
# Importa o RichHandler para logs coloridos no terminal
from rich.logging import RichHandler
from ftc4.common.config import settings

# Constante para o nível de log padrão (ajuste conforme necessário)
DEFAULT_LOG_LEVEL = logging.INFO


def get_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger. Adiciona handlers (terminal com rich, arquivo padrão) 
    apenas se ainda não existirem.
    """
    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)

    # Evita adicionar handlers múltiplas vezes ao mesmo logger
    if not logger.handlers:
        
        # --- 1. Handler para Terminal (COM CORES e Formatação RICH) ---
        # O RichHandler cuida de cores, colunas, sintaxe highlighting e tracebacks
        rich_handler = RichHandler(
            # Configurações de exibição de colunas
            show_time=True,           
            show_level=True,          
            show_path=False,          # Geralmente mais limpo não mostrar o caminho completo no terminal
            # Configurações avançadas
            markup=True,              # Permite usar tags do Rich nas mensagens
            rich_tracebacks=True,     # Formatação bonita e detalhada para logger.exception()
            tracebacks_suppress=[logging, sys] # Opcional: Oculta frames internos do logger para focar no seu código
        )
        
        # Para o RichHandler, um formato simples é suficiente, pois ele formata o restante em colunas
        rich_format = logging.Formatter("%(name)s: %(message)s")
        rich_handler.setFormatter(rich_format)
        logger.addHandler(rich_handler)

        # --- 2. Handler para Arquivo (Seu Formato Original, SEM CORES ANSI) ---
        try:
            # Cria o diretório se não existir (boas práticas)
            log_file_path = settings.LOG_DIR / "app.log"
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_file_path, 
                encoding="utf-8"
            )
            
            # Mantenha o formato de arquivo detalhado (com data/hora)
            file_format = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)
            
        except Exception as e:
            # Se a configuração do arquivo falhar (ex: settings.LOG_DIR não existe/erro de permissão), 
            # loga no terminal (que já está configurado) e continua.
            logger.warning(f"Atenção: Não foi possível configurar o FileHandler: {e}")

    return logger