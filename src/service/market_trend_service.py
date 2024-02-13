from sqlalchemy.orm import Session
from data.models import MarketTrend as DBMarketTrend
from model.models import MarketTrend
from typing import List


def create_market_trend(db: Session, trend: MarketTrend) -> DBMarketTrend:
    db_trend = DBMarketTrend(**trend.dict())
    db.add(db_trend)
    db.commit()
    db.refresh(db_trend)
    return db_trend


def get_all_market_trends(db: Session) -> List[MarketTrend]:
    db_trends = db.query(DBMarketTrend).all()
    return [MarketTrend(**trend) for trend in db_trends]
