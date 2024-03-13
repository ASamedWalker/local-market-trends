from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID


class Market(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    location_description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    # Relationship to PriceRecord
    price_records: List["PriceRecord"] = Relationship(back_populates="market")


class GroceryItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    category: str
    image_url: Optional[str] = None
    # Relationship to PriceRecord
    price_records: List["PriceRecord"] = Relationship(back_populates="grocery_item")


class PriceRecord(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id: UUID = Field(foreign_key="groceryitem.id")
    market_id: UUID = Field(foreign_key="market.id")
    price: float
    date_recorded: datetime = Field(default_factory=datetime.utcnow)
    # Relationships
    grocery_item: Optional[GroceryItem] = Relationship(back_populates="price_records")
    market: Optional[Market] = Relationship(back_populates="price_records")


class SpecialOffer(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id: UUID = Field(foreign_key="groceryitem.id")
    description: str
    valid_from: datetime
    valid_to: datetime
    image_url: Optional[str] = None
    # Relationship to GroceryItem
    grocery_item: Optional[GroceryItem] = Relationship(back_populates="special_offers")
