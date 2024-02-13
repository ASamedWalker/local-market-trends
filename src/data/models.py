from sqlalchemy import Column, Integer, ForeignKey, String, Float, Enum, DateTime, func
from sqlalchemy.orm import relationship
from model.models import MarketType
from .database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    market_type = Column(Enum(MarketType), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class MarketTrend(Base):
    __tablename__ = "market_trends"

    id = Column(Integer, primary_key=True, index=True)
    market_type = Column(Enum(MarketType))
    trend_description = Column(String, index=True)


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    price = Column(Float)
    date = Column(DateTime)
    source = Column(String)

    listing = relationship("Listing", back_populates="price_history")
