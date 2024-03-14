# src/services/grocery_item_service.py
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

# import fake.grocery_item as grocery_item_db


from src.models.grocery_item import GroceryItem


async def create_grocery_item(
    session: AsyncSession, grocery_item: GroceryItem
) -> GroceryItem:
    try:
        session.add(grocery_item)
        await session.commit()
        await session.refresh(grocery_item)
        return grocery_item
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_grocery_item(
    session: AsyncSession, grocery_item_id: UUID
) -> Optional[GroceryItem]:
    try:
        result = await session.get(GroceryItem, grocery_item_id)
        if not result:
            raise HTTPException(status_code=404, detail="Grocery item not found")
        return result
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_grocery_items(session: AsyncSession) -> List[GroceryItem]:
    try:
        result = await session.execute(select(GroceryItem))
        grocery_items = result.scalars().all()
        return grocery_items
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_grocery_item(
    session: AsyncSession, grocery_item_id: UUID, grocery_item_data: GroceryItem
) -> Optional[GroceryItem]:
    try:
        grocery_item = await session.get(GroceryItem, grocery_item_id)
        if grocery_item:
            grocery_item_data.id = grocery_item_id  # Ensure ID remains unchanged
            await session.merge(grocery_item_data)
            await session.commit()
            return await session.get(GroceryItem, grocery_item_id)
        return None
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_grocery_item(
    session: AsyncSession, grocery_item_id: UUID
) -> Optional[GroceryItem]:
    try:
        grocery_item = await session.get(GroceryItem, grocery_item_id)
        if grocery_item:
            await session.delete(grocery_item)
            await session.commit()
            return grocery_item
        return None
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
