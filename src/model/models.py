from pydantic import BaseModel, validator
from sqlalchemy.orm import relationship
from typing import Optional
from enum import Enum


class MarketType(str, Enum):
    real_estate = "real estate"
    retail = "retail"
    services = "services"
    local_foods = "local_foods"


class Listing(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    price_history = relationship("PriceHistory", order_by=PriceHistory.date, back_populates="listing")
    market_type: MarketType

    @validator("title")
    def title_must_be_longer_than(cls, value):
        if len(value) < 5:
            raise ValueError("Title must be at least 5 characters long")
        return value

    @validator("price")
    def price_must_be_reasonable(cls, value):
        if value <= 0 or value > 10000:
            raise ValueError("Price must be greater than 0 and less than 10000")
        return value


class MarketTrend(BaseModel):
    market_type: MarketType
    trend_description: str
