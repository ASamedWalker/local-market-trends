from fastapi import Depends, APIRouter
from sqlmodel import Session
from uuid import UUID, uuid4

from src.data.database import (
    get_session,
)  # Make sure this import path matches your project structure

router = APIRouter()


@router.get("/grocery_item/")
def read_root(db: Session = Depends(get_session)):
    # item = GroceryItem(name="apple", description="A fruit")
    return {"id": uuid4(), "name": "apple", "description": "A fruit"}
