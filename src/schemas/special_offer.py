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
