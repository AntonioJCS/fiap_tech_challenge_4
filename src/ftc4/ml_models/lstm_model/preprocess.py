from __future__ import annotations
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

class SeriesPreprocessor:
    def __init__(self, lookback: int = 60):
        self.lookback = lookback
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def fit_transform(self, series: np.ndarray) -> np.ndarray:
        series = series.reshape(-1, 1)
        return self.scaler.fit_transform(series)

    def transform(self, series: np.ndarray) -> np.ndarray:
        series = series.reshape(-1, 1)
        return self.scaler.transform(series)

    def inverse_transform(self, series: np.ndarray) -> np.ndarray:
        return self.scaler.inverse_transform(series.reshape(-1, 1)).ravel()

    def build_windows(self, scaled: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        X, y = [], []
        for i in range(self.lookback, len(scaled)):
            X.append(scaled[i - self.lookback:i, 0])
            y.append(scaled[i, 0])
        X = np.array(X)
        y = np.array(y)
        # (batch, seq, feat)
        return X.reshape((X.shape[0], X.shape[1], 1)), y