from fastapi import FastAPI
from api.v1.routers.stock_market import stock_market_router 

app = FastAPI()

app.include_router(stock_market_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
