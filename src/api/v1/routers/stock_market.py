from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data_pipeline.database.connection import get_db
from api.v1.schemas.stock_market_prices import StockMarketPriceBatch
from data_pipeline.sources.yfinance_source import fetch_stock_market_prices
from data_pipeline.crud.stock_market_prices import insert_many_prices

stock_market_router = APIRouter()

@stock_market_router.post("/insert_batch")
def insert_batch(
    payload: StockMarketPriceBatch,
    db: Session = Depends(get_db)
):
    try:
        insert_many_prices(db, payload.data)
        return {"message":"Lote inserido com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))