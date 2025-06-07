from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from src.config import DATABASE_DIR, SQLALCHEMY_DATABASE_URL


# 1. Conexão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. Base para classes ORM
Base = declarative_base()


def create_database():
    """
    Verifica se o diretorio e o banco de dados existe e os cria se necessário
    """
    if not DATABASE_DIR.exists():
        DATABASE_DIR.mkdir()

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_database()

