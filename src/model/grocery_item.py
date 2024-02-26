from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID, uuid4


class GroceryItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    category: str
    price_records: List["PriceRecord"] = Relationship(back_populates="grocery_item")
