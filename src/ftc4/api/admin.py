from fastapi import FastAPI
from ftc4.api.v1.routers.stock_market import stock_market_router 

app = FastAPI(title="Tech Challenge 4 - Admin API", version="1.0")

app.include_router(stock_market_router, prefix='/stock', tags=["Stock Market"])