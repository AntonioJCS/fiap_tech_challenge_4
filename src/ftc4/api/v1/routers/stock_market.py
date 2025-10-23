import pandas as pd
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ftc4.data_pipeline.database.connection import get_db
from ftc4.api.v1.schemas.stock_market_prices import StockMarketPriceBatch, StockPriceBase
from ftc4.data_pipeline.sources.yfinance_source import fetch_stock_market_prices
from ftc4.data_pipeline.crud.stock_market_prices import insert_many_prices
from datetime import datetime

# Importa a função do logger
from ftc4.common.logger import get_logger

# 1. Inicializa o Logger no módulo
# Isso garante que o logger seja criado uma única vez ao carregar o módulo.
logger = get_logger(__name__)

stock_market_router = APIRouter()

# -----------------------------------------------
# Rota 1: fetch_and_insert
# -----------------------------------------------
@stock_market_router.post("/fetch_insert")
def fetch_and_insert(
    ticker: str = Query(..., description="Ticker, ex: NVDA"),
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str | None = Query(None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    try:
        logger.info(f"Iniciando coleta para {ticker} de {start_date} até {end_date or 'hoje'}.")
        
        # ... (Seu código de busca, normalização e validação aqui) ...
        # (Seus passos 1 a 6 são mantidos intactos)
        
        # 1) Busca no yfinance
        df = fetch_stock_market_prices(ticker, start_date, end_date)

        # 2) Normaliza colunas esperadas
        #    (se vier indexado por data, traz pro corpo)
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
            # Opcional: Logar erro específico antes de levantar HTTPException
            logger.error(f"Erro de dados para {ticker}: Colunas ausentes do yfinance: {missing}")
            raise HTTPException(status_code=500, detail=f"Colunas ausentes do yfinance: {missing}")

        if df.empty:
            logger.warning(f"Coleta para {ticker} não retornou dados no período.")
            raise HTTPException(status_code=404, detail="Sem dados retornados para o período informado.")

        # 4) Limpeza de NaN e tipos
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date", "close", "high", "low", "open"]).copy()
        if df.empty:
            logger.error(f"Coleta para {ticker}: Todos os registros foram removidos por NaN em OHLC.")
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
            # Tenta converter, se der erro, loga e pula o registro (erros silenciosos aqui!)
            try:
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
            except Exception as item_e:
                # Loga o registro problemático e o erro, mas não interrompe o loop
                logger.error(f"Erro ao converter registro para Pydantic (Ticker: {r.get('ticker')}, Data: {r.get('date')}): {item_e}")
        
        if not data:
            logger.error(f"Coleta para {ticker}: Nenhum registro válido após limpeza/validação/conversão.")
            raise HTTPException(status_code=400, detail="Nenhum registro válido após limpeza/validação.")

        # 7) Persiste
        insert_many_prices(db, data)
        
        logger.info(
            f"Coleta e inserção de {len(data)} registros para {ticker.upper()} concluída com sucesso. "
            f"Período: {df['date'].min().strftime('%Y-%m-%d')} a {df['date'].max().strftime('%Y-%m-%d')}."
        )
        return {
            "message": "Coletado e inserido com sucesso",
            "ticker": ticker.upper(),
            "records": len(data),
            "first_date": df["date"].min().strftime("%Y-%m-%d"),
            "last_date": df["date"].max().strftime("%Y-%m-%d"),
        }
    except HTTPException:
        # Repassa exceções HTTPException já lançadas (e possivelmente logadas no passo 3/4)
        raise
    except Exception as e:
        # 2. Loga o erro GERAL com stack trace completa (catch-all)
        # Isso capturará erros em 'fetch_stock_market_prices' ou 'insert_many_prices'
        logger.exception(f"Erro inesperado no fetch_insert para ticker={ticker}")
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------
# Rota 2: insert_batch
# -----------------------------------------------
@stock_market_router.post("/insert_batch")
def insert_batch(payload: StockMarketPriceBatch, db: Session = Depends(get_db)):
    try:
        insert_many_prices(db, payload.data)
        # Opcional: Logar sucesso com nível INFO, útil para auditoria
        logger.info(f"Lote de {len(payload.data)} registros inserido com sucesso via /insert_batch.")
        return {"message": "Lote inserido com sucesso", "records": len(payload.data)}
    except Exception as e:
        # 2. Loga o erro com stack trace completa
        # O 'exc_info=True' ou usar logger.exception() faz isso automaticamente.
        logger.exception("Erro ao inserir lote via /insert_batch.")
        raise HTTPException(status_code=500, detail=str(e))