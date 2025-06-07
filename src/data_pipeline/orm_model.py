from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RawStockMarketPrices(Base):
    __tablename__ = "raw_stock_market_prices"
    id = Column(Integer, primary_key=True, index=True)
    Date = Column(Date, nullable=False)
    Ticker = Column(String, nullable=False)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Open = Column(Float)
    Volume  = Column(Integer)


