from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from uuid import UUID, uuid4


class Listing(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    price: float
    category_id: Optional[UUID] = Field(foreign_key="category.id")
    location_id: Optional[UUID] = Field(foreign_key="location.id")
    category: "Category" = Relationship(back_populates="listings")
    location: "Location" = Relationship(back_populates="listings")
