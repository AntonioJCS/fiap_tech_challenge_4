import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env variables to Environ
load_dotenv()

# Project Base Dir
BASE_DIR = (Path(__file__).parent.parent).resolve() # src/
PROJECT_ROOT_DIR = BASE_DIR.parent 

# Local Data Base
DATABASE_DIR = Path(os.getenv("DATABASE_DIR", PROJECT_ROOT_DIR / 'data'))
DATABASE_PATH = DATABASE_DIR / 'stock_market.db'
