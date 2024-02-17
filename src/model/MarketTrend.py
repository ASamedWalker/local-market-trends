from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class MarketTrend(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    start_date: date
    end_date: date
    affected_categories: List[str] = []
