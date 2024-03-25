from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class SpecialOfferCreate(BaseModel):
    grocery_item_id: UUID
    description: str
    valid_from: datetime
    valid_to: datetime
    image_url: Optional[str] = None


class SpecialOfferUpdate(BaseModel):
    grocery_item_id: Optional[UUID] = None
    description: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    image_url: Optional[str] = None
