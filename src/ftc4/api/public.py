from fastapi import FastAPI
from contextlib import asynccontextmanager

from ftc4.data_pipeline.database.init_db import init_db
from ftc4.api.v1.routers.stock_market import stock_market_router
from ftc4.api.v1.routers.model_lstm import router as lstm_router
from ftc4.common.logger import get_logger


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Tech Challenge 4 - Public API", version="1.0", lifespan=lifespan)

# Checagem de estado de funcionamento da API
@app.get("/health")
def health():
    logger.info({"status": "ok"})
    return {"status": "ok"}

# Reutiliza rotas de bolsa (inserção) para facilitar testes
app.include_router(stock_market_router, prefix='/stock', tags=["Stock Market"])

# Modelos LSTM
app.include_router(lstm_router)