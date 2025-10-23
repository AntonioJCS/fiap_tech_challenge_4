from ftc4.common.config import settings

ARTIFACTS_DIR = settings.ML_MODELS_DIR / "lstm_model"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)