from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID, uuid4



class Market(SQLModel, table=True):
    __tablename__ = "market"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    location_description: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    price_records: List["PriceRecord"] = Relationship(back_populates="market")
