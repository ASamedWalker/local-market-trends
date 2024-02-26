from sqlmodel import Field, SQLModel, Relationship
from datatime import datetime
from typing import Optional
from uuid import UUID


class PriceRecord(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    grocery_item_id: UUID = Field(foreign_key="groceryitem.id")
    market_id: UUID = Field(foreign_key="market.id")
    price: float
    date_recorded: datetime = Field(default_factory=datetime.utcnow)
    grocery_item: Optional["GroceryItem"] = Relationship(back_populates="price_records")
    market: Optional["Market"] = Relationship(back_populates="price_records")
