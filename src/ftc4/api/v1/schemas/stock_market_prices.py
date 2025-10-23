from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import List

class StockPriceBase(BaseModel):
    """Schema base para StockPrice"""
    date: datetime = Field(..., description="Data do preço da ação")
    ticker: str = Field(..., min_length=1, max_length=16, description="Ticker do ativo")
    close: float = Field(..., gt=0, description="Preço de fechamento")
    high: float = Field(..., gt=0, description="Preço máximo do dia")
    low: float = Field(..., gt=0, description="Preço mínimo do dia")
    open: float = Field(..., gt=0, description="Preço de abertura")
    volume: int = Field(..., ge=0, description="Volume de negociação")

    @field_validator("ticker")
    @classmethod
    def ticker_upper(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Ticker não pode ser vazio")
        return v.upper()

    @model_validator(mode="after")
    def check_ohlc(self) -> "StockPriceBase":
        # Regras de coerência entre campos
        if self.high < self.low:
            raise ValueError("Preço máximo (high) não pode ser menor que o mínimo (low)")
        if self.low > self.open or self.low > self.close:
            raise ValueError("Preço mínimo (low) não pode ser maior que open/close")
        if self.high < self.open or self.high < self.close:
            raise ValueError("Preço máximo (high) não pode ser menor que open/close")
        return self

class StockMarketPriceBatch(BaseModel):
    data: List[StockPriceBase]
