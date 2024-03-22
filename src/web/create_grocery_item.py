from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session
from uuid import UUID, uuid4

from src.data.database import (
    get_session,
)
from src.models import GroceryItem


router = APIRouter()


@router.post("/grocery_item/", response_model=GroceryItem)
async def create_grocery_item_endpoint(
    item: GroceryItem, db: Session = Depends(get_session)
):
    try:
        db_item = GroceryItem(
            id=uuid4(),
            name=item.name,
            description=item.description,
            category=item.category,
        )
        db.add(db_item)  # Add the item to the session
        db.commit()  # Commit the transaction
        db.refresh(db_item)
        return await db_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
