from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class GroceryItem(SQLModel, table=True):
    __tablename__ = "grocery_item"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    category: str
    image_url: Optional[str] = Field(default=None)
    price_records: List["PriceRecord"] = Relationship(back_populates="grocery_item")
    special_offers: List["SpecialOffer"] = Relationship(
        back_populates="grocery_item"
    )  # Use the imported SpecialOffer class


class Market(SQLModel, table=True):
    __tablename__ = "market"
    id:  Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    location_description: str = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    # Define a relationship with the PriceRecord model
    price_records: List["PriceRecord"] = Relationship(back_populates="market")


class PriceRecord(SQLModel, table=True):
    __tablename__ = "price_record"
    id:  Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id:  Optional[UUID] = Field(foreign_key="grocery_item.id")
    market_id:  Optional[UUID] = Field(foreign_key="market.id")
    price: Optional[float]
    date_recorded: datetime = Field(default_factory=datetime.utcnow)
    is_promotional: bool = Field(default=False)
    promotional_details: str = Field(default=None)
    grocery_item: Optional["GroceryItem"] = Relationship(back_populates="price_records")
    market: Optional["Market"] = Relationship(back_populates="price_records")


class SpecialOffer(SQLModel, table=True):
    __tablename__ = "special_offer"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id: Optional[UUID] = Field(foreign_key="grocery_item.id")
    description: str
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_to: datetime = Field(default_factory=datetime.utcnow)
    image_url: Optional[str] = None

    # Ensure that valid_from is before valid_to
    def is_valid_offer(self) -> bool:
        return self.valid_from <= self.valid_to

    grocery_item: Optional["GroceryItem"] = Relationship(
        back_populates="special_offers"
    )
