from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from uuid import UUID, uuid4

from src.data.database import (
    get_session,
)
from src.models import GroceryItem

router = APIRouter()


@router.post("/grocery_item/", response_model=GroceryItem)
def read_root(item: GroceryItem, db: Session = Depends(get_session)):
    db_item = GroceryItem(id=uuid4(), name=item.name, description=item.description)
    return db_item
