from __future__ import annotations
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from pathlib import Path
from ftc4.ml_models.lstm_model.model import LSTMForecaster
from ftc4.ml_models.lstm_model.preprocess import SeriesPreprocessor
from ftc4.ml_models import lstm_model

class Trainer:
    def __init__(self, lookback: int = 60, lr: float = 1e-3, epochs: int = 20, batch_size: int = 64):
        self.pp = SeriesPreprocessor(lookback=lookback)
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size

    def fit(self, series: np.ndarray, device: str | None = None):
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        scaled = self.pp.fit_transform(series)
        X, y = self.pp.build_windows(scaled)
        X_t = torch.tensor(X, dtype=torch.float32).to(device)
        y_t = torch.tensor(y, dtype=torch.float32).unsqueeze(1).to(device)

        ds = TensorDataset(X_t, y_t)
        dl = DataLoader(ds, batch_size=self.batch_size, shuffle=True)

        model = LSTMForecaster().to(device)
        opt = torch.optim.Adam(model.parameters(), lr=self.lr)
        loss_fn = nn.MSELoss()

        model.train()
        for epoch in range(self.epochs):
            epoch_loss = 0.0
            for xb, yb in dl:
                opt.zero_grad()
                preds = model(xb)
                loss = loss_fn(preds, yb)
                loss.backward()
                opt.step()
                epoch_loss += loss.item() * xb.size(0)
            epoch_loss /= len(ds)
            if (epoch + 1) % 5 == 0:
                print(f"[epoch {epoch+1}] loss={epoch_loss:.6f}")

        # salvar
        torch.save(model.state_dict(), lstm_model.ARTIFACTS_DIR / "lstm.pt")
        import joblib
        joblib.dump(self.pp, lstm_model.ARTIFACTS_DIR / "preprocessor.joblib")
        return model