from fastapi import APIRouter
from data_pipeline.sources.yfinance_source import fetch_stock_market_prices

stock_market_router = APIRouter()

@stock_market_router.post("/extract/yfinance")
def trigger_yfinance_extraction():
    fetch_stock_market_prices('NVDA', '2022-01-01')
    return {"status": "ok"}