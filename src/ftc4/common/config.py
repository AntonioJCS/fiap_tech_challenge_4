import os
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass

# Load .env variables to Environ
load_dotenv(override=True)


@dataclass(frozen=True)
class Settings:
    # Ambiente
    APP_ENV: str = os.getenv("APP_ENV", "dev")

    # Diretório raiz do projeto
    BASE_DIR: Path = Path(__file__).parents[3].resolve()

    # Armazenamento
    DATABASE_DIR: Path = Path(os.getenv("DATA_DIR", BASE_DIR / "data")).resolve()
    DATABASE_PATH: Path = Path(DATABASE_DIR / "stock_market.db").resolve()
    ARTIFACTS_DIR: Path = Path(os.getenv("ARTIFACTS_DIR", DATABASE_DIR / "artifacts")).resolve()
    ML_MODELS_DIR: Path = Path(ARTIFACTS_DIR / "ml_models").resolve()

    # Logs
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", BASE_DIR / "logs")).resolve()

# Instanciando configurações
settings = Settings()


# Cria diretórios automaticamente
dirs = [settings.LOG_DIR, settings.DATABASE_DIR, settings.ARTIFACTS_DIR]
for p in dirs:
    p.mkdir(parents=True, exist_ok=True)


def main():
    from dataclasses import asdict
    import json

    # Converte a instância para um dicionário (dict)
    settings_dict = asdict(settings)

    # Printa o dicionário formatado
    print(json.dumps(settings_dict, indent=4, default=str))


if __name__ == "__main__":
    main()
