from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
import numpy as np

from ftc4.data_pipeline.database.connection import get_db
from ftc4.data_pipeline.orm_models.stock_market import StockPrice
from ftc4.ml_models.lstm_model.train import Trainer
from ftc4.ml_models.lstm_model.predict import predict_next
from ftc4.common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/lstm", tags=["LSTM"])

@router.post("/train")
def train_model(
    ticker: str = Query(..., description="Ticker, ex: NVDA"),
    lookback: int = Query(60, ge=5, le=200),
    db: Session = Depends(get_db),
):
    # carrega série do banco
    q = (
        select(StockPrice.close)
        .where(StockPrice.ticker == ticker.upper())
        .order_by(StockPrice.date.asc())
    )
    values = [float(x[0]) for x in db.execute(q).all()]
    if len(values) < lookback + 5:
        error_message = f"Série insuficiente para treino. Tamanho atual: {len(values)}, Requerido: {lookback + 5}."
        logger.error(error_message)
        raise HTTPException(status_code=400, detail="Série de dados insuficiente para o treinamento. Verifique o tamanho da sua entrada.")

    series = np.array(values, dtype=float)
    Trainer(lookback=lookback).fit(series)         # salva artefatos em /artifacts
    return_msg = {"message": "Modelo treinado com sucesso", "ticker": ticker.upper(), "n_obs": len(series)}
    logger.info(return_msg)
    return return_msg


@router.get("/predict")
def predict(
    steps: int = Query(5, ge=1, le=30),
    ticker: str = Query(...),
    db: Session = Depends(get_db),
):
    q = (
        select(StockPrice.close)
        .where(StockPrice.ticker == ticker.upper())
        .order_by(StockPrice.date.asc())
    )
    values = [float(x[0]) for x in db.execute(q).all()]
    if not values:
        error_message = "Sem dados no banco para este ticker"
        logger.error(error_message)
        raise HTTPException(status_code=404, detail="Sem dados no banco para este ticker")

    preds = predict_next(np.array(values, dtype=float), n_steps=steps)
    logger.info(f"Os proximos {steps} valores de fechamento foram previstos. {str(preds.tolist()[0:3]).replace(']', ', ...]')}")
    return {"ticker": ticker.upper(), "steps": steps, "predictions": preds.tolist()}
