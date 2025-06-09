import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env variables to Environ
load_dotenv()

# Project Base Dir
BASE_DIR = (Path(__file__).parent.parent).resolve()
PROJECT_DIR = BASE_DIR.parent # src/

# Local Data Base
DATABASE_DIR = Path(os.getenv("DATABASE_DIR", PROJECT_DIR / 'data'))
DATABASE_STOCK_MARKET_PATH = Path(DATABASE_DIR) / "stock_market.db"
DATABASE_STOCK_MARKET_URL = f"sqlite:///{DATABASE_STOCK_MARKET_PATH.as_posix()}"
