from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class SpecialOffer(SQLModel, table=True):
    __tablename__ = "special_offer"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id: UUID = Field(foreign_key="groceryitem.id")
    description: str
    valid_from: datetime
    valid_to: datetime
    image_url: Optional[str] = None

    # Ensure that valid_from is before valid_to
    def is_valid_offer(self) -> bool:
        return self.valid_from <= self.valid_to

    grocery_item: Optional["GroceryItem"] = Relationship(
        back_populates="special_offers"
    )
