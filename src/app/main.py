from fastapi import FastAPI
from features.stock_prediction import monitoring_router, ml_performance_router, stock_predict_router

app = FastAPI(
    title="Meu Projeto FastAPI",
    description="API de exemplo com uso de routers.",
    version="1.0.0"
)

# Inclui o router
app.include_router(monitoring_router) #prefix="/exemplo", tags=["Exemplo"] não foram usados pois já esta declarados no router
app.include_router(ml_performance_router)
app.include_router(stock_predict_router)


# Rota raiz só para teste
@app.get("/")
def read_root():
    return {"msg": "Hello, FastAPI com routers!"}
