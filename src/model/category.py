from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID, uuid4


class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    listings: List["Listing"] = Relationship(back_populates="category")
