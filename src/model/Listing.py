from pydantic import BaseModel, HttpUrl
from typing import Optional


class Listing(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    price: float
    category: str  # Consider using an Enum for predefined categories
    url: Optional[HttpUrl] = None  # Optional URL to the listing
