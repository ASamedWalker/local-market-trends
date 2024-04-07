from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TypeVar, Generic, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4



class GroceryItem(SQLModel, table=True):
    __tablename__ = "grocery_item"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    category: str
    image_url: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None, description="Unit of measure for the item, e.g., per lb, per kg, pack of 10")
    price_records: List["PriceRecord"] = Relationship(back_populates="grocery_item")
    special_offers: List["SpecialOffer"] = Relationship(
        back_populates="grocery_item"
    )
    reviews: List["Review"] = Relationship(back_populates="grocery_item")


class Market(SQLModel, table=True):
    __tablename__ = "market"
    id:  Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    location_description: str = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    opeating_hours: Optional[str] = Field(default=None)
    rating: Optional[float] = Field(default=None)
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
    valid_from: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The start date of the price validity")
    valid_to: Optional[datetime] = Field(default=None, description="The end date of the price validity")
    promotional_details: Optional[str] = Field(default=None)
    grocery_item: Optional["GroceryItem"] = Relationship(back_populates="price_records")
    market: Optional["Market"] = Relationship(back_populates="price_records")



class SpecialOfferGroceryItemLink(SQLModel, table=True):
    special_offer_id: UUID = Field(default=None, foreign_key="special_offer.id", primary_key=True)
    grocery_item_id: UUID = Field(default=None, foreign_key="grocery_item.id", primary_key=True)


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
        back_populates="special_offers", link_model=SpecialOfferGroceryItemLink
    )


class Review(SQLModel, table=True):
    __tablename__ = "review"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    grocery_item_id: UUID = Field(foreign_key="grocery_item.id")
    rating: int = Field(ge=1, le=5)  # Ratings between 1 and 5
    comment: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    upvotes: int = Field(default=0, description="Number of upvotes indicating the review's usefulness")
    downvotes: int = Field(default=0, description="Number of downvotes indicating the review's lack of usefulness")
    # Relationship back to the GroceryItem
    grocery_item: "GroceryItem" = Relationship(back_populates="reviews")

