from fastapi import FastAPI
from ftc4.api.v1.routers.stock_market import stock_market_router 
from contextlib import asynccontextmanager
from ftc4.data_pipeline.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Tech Challenge 4 - Admin API", version="1.0", lifespan=lifespan)

app.include_router(stock_market_router, prefix='/stock', tags=["Stock Market"])