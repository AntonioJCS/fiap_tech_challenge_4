from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

# Banco de dados
DATABASE_DIR = BASE_DIR / "db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{(DATABASE_DIR / 'finance.db').as_posix()}"
