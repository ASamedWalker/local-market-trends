from fastapi import APIRouter
from typing import List
from model.MarketTrend import MarketTrend

router = APIRouter()

# Dummy data for demonstration
fake_market_trends_db = [
    {
        "id": 1,
        "title": "Summer Electronics Sale",
        "description": "Up to 50% off on select electronics.",
        "start_date": "2023-06-01",
        "end_date": "2023-06-30",
        "affected_categories": ["Electronics"],
    }
]


@router.get("/market-trends/", response_model=List[MarketTrend])
async def read_market_trends():
    return fake_market_trends_db
