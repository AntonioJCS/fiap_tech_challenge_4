from fastapi import FastAPI
from api.v1.routers.stock_market import stock_market_router
from api.v1.routers.model_lstm import router as lstm_router

app = FastAPI(title="Tech Challenge 4 - Public API", version="1.0")

# Checagem de estado de funcionamento da API
@app.get("/health")
def health():
    return {"status": "ok"}

# Reutiliza rotas de bolsa (inserção) para facilitar testes
app.include_router(stock_market_router, prefix='/stock', tags=["Stock Market"])

# Modelos LSTM
app.include_router(lstm_router)