import importlib
from pathlib import Path
from ftc4.data_pipeline.database.connection import Base, engine
from ftc4.common.config import settings
from ftc4.common.logger import get_logger

logger = get_logger(__name__)

def import_all_models():
    """
    Carrega todos os modelos ORM disponíveis para que o SQLAlchemy
    reconheça as tabelas na chamada Base.metadata.create_all.
    """
    models_path = (Path(__file__).parents[2] / "orm_models").resolve()
    for file in models_path.glob("*.py"):
        if file.name.startswith("__"):
            continue
        module = f"data_pipeline.orm_models.{file.stem}"
        importlib.import_module(module)


def init_db():
    logger.info("Verificando diretório do banco de dados...")
    settings.DATABASE_DIR.mkdir(exist_ok=True)

    logger.info("Importando modelos ORM...")
    import_all_models()

    logger.info("Verifica e cria todas as tabelas no banco...")
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()