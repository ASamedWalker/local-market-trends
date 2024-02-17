from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional


class Deal(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    valid_until: Optional[date] = None
    discount_rate: float  # A percentage value representing the discount
    url: Optional[HttpUrl] = (
        None  # Optional URL to more information or to redeem the deal
    )
