from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from common.config import DATABASE_PATH

# URL do SQLite
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Criando o engine com echo opcional
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Gerador de sessão (tipado e thread-safe)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# Nova forma de criar Base (API 2.0)
class Base(DeclarativeBase):
    pass