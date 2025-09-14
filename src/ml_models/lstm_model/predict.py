# src/ml_models/lstm_model/predict.py
from __future__ import annotations
import numpy as np
import torch
from pathlib import Path
from ml_models.lstm_model.model import LSTMForecaster

ARTIFACTS_DIR = Path("src/ml_models/lstm_model/artifacts")

def load_artifacts():
    model = LSTMForecaster()
    model.load_state_dict(torch.load(ARTIFACTS_DIR / "lstm.pt", map_location="cpu"))
    model.eval()
    import joblib
    pp = joblib.load(ARTIFACTS_DIR / "preprocessor.joblib")
    return model, pp

@torch.no_grad()
def predict_next(series: np.ndarray, n_steps: int = 5):
    model, pp = load_artifacts()
    device = "cpu"
    scaled = pp.transform(series)

    # previsão recursiva
    window = scaled[-pp.lookback:].reshape(1, pp.lookback, 1)
    window = torch.tensor(window, dtype=torch.float32).to(device)

    preds_scaled = []
    for _ in range(n_steps):
        yhat = model(window).cpu().numpy().ravel()[0]
        preds_scaled.append(yhat)
        # shift janela
        new_window = np.concatenate([window.cpu().numpy().ravel()[1:], [yhat]])
        window = torch.tensor(new_window.reshape(1, pp.lookback, 1), dtype=torch.float32).to(device)

    preds = pp.inverse_transform(np.array(preds_scaled))
    return preds