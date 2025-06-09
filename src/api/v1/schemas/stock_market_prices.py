from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

class StockPriceBase(BaseModel):
    """Schema base para StockPrice"""
    date: date = Field(..., description="Data do preço da ação")
    ticker: str = Field(..., min_length=1, max_length=16, description="Código de negociação de um ativo ou derivativo na Bolsa de Valores")
    close: float = Field(..., gt=0, description="Preço de fechamento")
    high: float = Field(..., gt=0, description="Preço máximo do dia")
    low: float = Field(..., gt=0, description="Preço mínimo do dia")
    open: float = Field(..., gt=0, description="Preço de abertura")
    volume: int = Field(..., ge=0, description="Volume de negociação")
    
    @field_validator('ticker')
    def ticker_must_be_uppercase(cls, v):
        """Converte ticker para maiúsculo"""
        return v.upper().strip()
    
    @field_validator('high', 'low', 'open', 'close')
    def validate_prices(cls, v, values):
        """Valida se os preços são positivos e fazem sentido logicamente"""
        if v <= 0:
            raise ValueError('Preços devem ser maiores que zero')
        return round(v, 2)  # Arredonda para 2 casas decimais
    
    @field_validator('low')
    def low_must_be_reasonable(cls, v, values):
        """Valida se o preço mínimo não é maior que outros preços"""
        if 'high' in values and v > values['high']:
            raise ValueError('Preço mínimo não pode ser maior que o máximo')
        if 'open' in values and v > values['open']:
            raise ValueError('Preço mínimo não pode ser maior que abertura')
        if 'close' in values and v > values['close']:
            raise ValueError('Preço mínimo não pode ser maior que fechamento')
        return v
    
    @field_validator('high')
    def high_must_be_reasonable(cls, v, values):
        """Valida se o preço máximo não é menor que outros preços"""
        if 'low' in values and v < values['low']:
            raise ValueError('Preço máximo não pode ser menor que o mínimo')
        if 'open' in values and v < values['open']:
            raise ValueError('Preço máximo não pode ser menor que abertura')
        if 'close' in values and v < values['close']:
            raise ValueError('Preço máximo não pode ser menor que fechamento')
        return v

