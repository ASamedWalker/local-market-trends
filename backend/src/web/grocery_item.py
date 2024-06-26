from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from data.database import get_session
from services.grocery_item_service import (
    create_grocery_item,
    get_grocery_item,
    get_all_grocery_items,
    update_grocery_item,
    delete_grocery_item,
)


from models.all_models import GroceryItem


router = APIRouter(prefix="/grocery_items", tags=["grocery_items"])


@router.post("/", response_model=GroceryItem)
async def create_grocery_item_endpoint(
    grocery_item: GroceryItem, session: AsyncSession = Depends(get_session)
) -> GroceryItem:
    return await create_grocery_item(session, grocery_item)


@router.get("/", response_model=List[GroceryItem])
async def get_all_grocery_items_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[GroceryItem]:
    return await get_all_grocery_items(session)


@router.get("/{grocery_item_id}", response_model=GroceryItem)
async def get_grocery_item_endpoint(
    grocery_item_id: UUID, session: AsyncSession = Depends(get_session)
) -> GroceryItem:
    grocery_item = await get_grocery_item(session, grocery_item_id)
    if not grocery_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Grocery item not found"
        )
    return grocery_item


@router.put("/{grocery_item_id}", response_model=GroceryItem)
async def update_grocery_item_endpoint(
    grocery_item_id: UUID,
    grocery_item: GroceryItem,
    session: AsyncSession = Depends(get_session),
) -> GroceryItem:

    grocery_item_dict = grocery_item.model_dump()

    updated_grocery_item = await update_grocery_item(
        session, grocery_item_id, grocery_item_dict
    )
    if not updated_grocery_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Grocery item not found"
        )
    return updated_grocery_item


@router.delete("/{grocery_item_id}", response_model=GroceryItem)
async def delete_grocery_item_endpoint(
    grocery_item_id: UUID, session: AsyncSession = Depends(get_session)
) -> GroceryItem:
    deleted_grocery_item = await delete_grocery_item(session, grocery_item_id)
    if not deleted_grocery_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Grocery item not found"
        )
    return deleted_grocery_item

