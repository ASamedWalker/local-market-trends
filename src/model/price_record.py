from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class PriceRecord(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id: UUID = Field(foreign_key="groceryitem.id")
    market_id: UUID = Field(foreign_key="market.id")
    price: float
    date_recorded: datetime = Field(default_factory=datetime.utcnow)
    grocery_item: Optional["GroceryItem"] = Relationship(back_populates="price_records")
    market: Optional["Market"] = Relationship(back_populates="price_records")
