from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from ftc4.common.config import settings
from sqlalchemy import URL
from ftc4.common.logger import get_logger

logger = get_logger(__name__)

# URL do SQLite
url = URL.create(drivername='sqlite', database=settings.DATABASE_PATH.as_posix())

# Criando o engine com echo opcional
engine = create_engine(url, echo=False, connect_args={"check_same_thread": False})

# Gerador de sessão (tipado e thread-safe) (garante que cada thread tenha sua própria sessão)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# Nova forma de criar Base (API 2.0)
class Base(DeclarativeBase):
    pass

def get_db():
    """Função para gestão de sessões independentes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    logger.info(url)
    logger.info(engine)

