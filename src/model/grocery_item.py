from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID


class GroceryItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    category: str
    price_records: List["PriceRecord"] = Relationship(back_populates="grocery_item")
