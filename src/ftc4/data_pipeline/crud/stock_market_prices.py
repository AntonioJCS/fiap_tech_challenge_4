from sqlalchemy.orm import Session
from ftc4.data_pipeline.orm_models.stock_market import StockPrice

def insert_many_prices(db: Session, data_list: list):
    db_prices = [StockPrice(**item.dict()) for item in data_list]
    db.add_all(db_prices)
    db.commit()
