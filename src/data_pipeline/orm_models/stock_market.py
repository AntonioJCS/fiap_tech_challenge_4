from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.types import DECIMAL
from data_pipeline.orm_models import Base

class StockPrice(Base):
    __tablename__ = 'stock_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, index=True)
    ticker = Column(String(16), nullable=False, index=True)
    close = Column(DECIMAL(10, 2), nullable=False)
    high = Column(DECIMAL(10, 2), nullable=False)
    low = Column(DECIMAL(10, 2), nullable=False)
    open = Column(DECIMAL(10, 2), nullable=False)
    volume = Column(Integer, nullable=False)

    def __repr__(self):
        return (f"<StockPrice(date={self.date}, ticker={self.ticker}, "
                f"close={self.close}, high={self.high}, low={self.low}, "
                f"open={self.open}, volume={self.volume})>")