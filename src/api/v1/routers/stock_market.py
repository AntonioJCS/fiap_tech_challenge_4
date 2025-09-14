import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from data_pipeline.database.connection import get_db
from api.v1.schemas.stock_market_prices import StockMarketPriceBatch, StockPriceBase
from data_pipeline.sources.yfinance_source import fetch_stock_market_prices
from data_pipeline.crud.stock_market_prices import insert_many_prices
from datetime import datetime

stock_market_router = APIRouter()

@stock_market_router.post("/insert_batch")
def insert_batch(payload: StockMarketPriceBatch, db: Session = Depends(get_db)):
    try:
        insert_many_prices(db, payload.data)
        return {"message": "Lote inserido com sucesso", "records": len(payload.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@stock_market_router.post("/fetch_insert")
def fetch_and_insert(
    ticker: str = Query(..., description="Ticker, ex: NVDA"),
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str | None = Query(None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    try:
        # 1) Busca no yfinance
        df = fetch_stock_market_prices(ticker, start_date, end_date)

        # 2) Normaliza colunas esperadas
        #    (se vier indexado por data, traz pro corpo)
        if "Date" not in df.columns and df.index.name == "Date":
            df = df.reset_index()

        rename_map = {
            "Date": "date", "Close": "close", "High": "high",
            "Low": "low", "Open": "open", "Volume": "volume"
        }
        # algumas versões trazem em minúsculas, reforça mapeamento
        lower_map = {c.lower(): c for c in df.columns}
        df.columns = [lower_map.get(c.lower(), c) for c in df.columns]
        df = df.rename(columns=rename_map)

        # 3) Checagens mínimas
        required = ["date", "close", "high", "low", "open"]
        if any(col not in df.columns for col in required):
            missing = [c for c in required if c not in df.columns]
            raise HTTPException(status_code=500, detail=f"Colunas ausentes do yfinance: {missing}")

        if df.empty:
            raise HTTPException(status_code=404, detail="Sem dados retornados para o período informado.")

        # 4) Limpeza de NaN e tipos
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date", "close", "high", "low", "open"]).copy()
        if df.empty:
            raise HTTPException(status_code=400, detail="Todos os registros vieram com NaN em OHLC.")

        for c in ["close", "high", "low", "open"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        # volume pode ser float/NaN: normaliza pra int
        if "volume" not in df.columns:
            df["volume"] = 0
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int)

        # 5) Adiciona ticker em upper e ordena
        df["ticker"] = ticker.upper()
        df = df.sort_values("date")

        # 6) Constrói payload p/ Pydantic
        data = []
        for _, r in df.iterrows():
            data.append(
                StockPriceBase(
                    date=r["date"].to_pydatetime(),
                    ticker=r["ticker"],
                    close=float(r["close"]),
                    high=float(r["high"]),
                    low=float(r["low"]),
                    open=float(r["open"]),
                    volume=int(r["volume"]),
                )
            )

        if not data:
            raise HTTPException(status_code=400, detail="Nenhum registro válido após limpeza/validação.")

        # 7) Persiste
        insert_many_prices(db, data)
        return {
            "message": "Coletado e inserido com sucesso",
            "ticker": ticker.upper(),
            "records": len(data),
            "first_date": df["date"].min().strftime("%Y-%m-%d"),
            "last_date": df["date"].max().strftime("%Y-%m-%d"),
        }
    except HTTPException:
        raise
    except Exception as e:
        # dica: logue o erro no arquivo
        from common.logger import get_logger
        logger = get_logger(__name__)
        logger.exception("Erro no fetch_insert")
        raise HTTPException(status_code=500, detail=str(e))