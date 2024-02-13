from fastapi import APIRouter
from model.models import MarketTrend
from service.market_trend_service import create_market_trend, get_all_market_trends
from typing import List

router = APIRouter(prefix="/market-trends")


# Dummy database
fake_market_trends_db = []


@router.post("/", response_model=MarketTrend)
async def create_market_trend_endpoint(trend: MarketTrend):
    return create_market_trend(trend)


@router.get("/", response_model=List[MarketTrend])
async def get_all_market_trends_endpoint():
    return get_all_market_trends()
