import numpy as np
from ftc4.ml_models.lstm_model.train import Trainer
from ftc4.ml_models.lstm_model.predict import predict_next

def test_lstm_train_predict_smoke():
    # série senoidal simples
    x = np.linspace(0, 50, 400)
    s = np.sin(x) + 10
    t = Trainer(lookback=20, epochs=1, batch_size=32)
    t.fit(s)
    preds = predict_next(s, n_steps=3)
    assert len(preds) == 3