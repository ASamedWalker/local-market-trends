from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID, uuid4


class Location(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    city: str
    state: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    listings: List["Listing"] = Relationship(back_populates="location")
