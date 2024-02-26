from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID


class Market(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    location_description: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    price_records: List["PriceRecord"] = Relationship(back_populates="market")
