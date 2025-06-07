from fastapi import APIRouter

stock_predict_router = APIRouter(
    prefix="/stock-predict",   # Prefixo para as rotas desse módulo
    tags=["Stock Predict"]     # Tag para a documentação
)

@stock_predict_router.get("/exemplo")
def exemplo_endpoint():
    return {"msg": "Endpoint de exemplo da funcionalidade stock-predict"}



monitoring_router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)

@monitoring_router.get("/health")
def check_health():
    return {"status": "ok"}

@monitoring_router.get("/metrics")
def get_metrics():
    return {"cpu_usage": "20%", "memory_usage": "45%"}



ml_performance_router = APIRouter(
    prefix="/ml-performance",
    tags=["ML Performance"]
)

@ml_performance_router.get("/accuracy")
def get_accuracy():
    # Exemplo de resposta estática, mas normalmente viria de uma função/DB
    return {"model": "LSTM", "accuracy": 0.92}

@ml_performance_router.get("/latency")
def get_latency():
    return {"model": "LSTM", "latency_ms": 35}

