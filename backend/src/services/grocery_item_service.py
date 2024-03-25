# src/services/grocery_item_service.py
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import logging


from models.all_models import GroceryItem

logger = logging.getLogger(__name__)


async def create_grocery_item(
    session: AsyncSession, grocery_item: GroceryItem
) -> GroceryItem:
    try:
        session.add(grocery_item)
        # logging.info("session has been added")
        await session.commit()
        # logging.info("session has been committed")
        await session.refresh(grocery_item)
        # logging.info("session has been refreshed")
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
        logger.error(f"Failed to retrieve grocery items: {e}")
    raise HTTPException(status_code=500, detail="Failed to retrieve grocery items")


async def update_grocery_item(
    session: AsyncSession, grocery_item_id: UUID, grocery_item_data: dict
) -> Optional[GroceryItem]:
    # Validate grocery_item_data
    if not isinstance(grocery_item_data, dict):
        raise HTTPException(
            status_code=400, detail="grocery_item_data must be a dictionary"
        )
    for key in grocery_item_data:
        if not hasattr(GroceryItem, key):
            raise HTTPException(status_code=400, detail=f"Invalid key: {key}")

    try:
        grocery_item = await session.get(GroceryItem, grocery_item_id)
        if not grocery_item:
            raise HTTPException(status_code=404, detail="Grocery item not found")

        for key, value in grocery_item_data.items():
            setattr(grocery_item, key, value)

        await session.commit()
        return grocery_item.model_dump()
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Failed to update grocery item due to constraint violation: {e}")
        raise HTTPException(
            status_code=400,
            detail="Failed to update grocery item due to constraint violation",
        )
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Failed to update grocery item: {e}")
        raise HTTPException(status_code=500, detail="A database error occurred")


async def delete_grocery_item(
    session: AsyncSession, grocery_item_id: UUID
) -> Optional[GroceryItem]:
    try:
        grocery_item = await session.get(GroceryItem, grocery_item_id)
        if grocery_item:
            await session.delete(grocery_item)
            await session.commit()
            return grocery_item
        else:
            raise HTTPException(status_code=404, detail="Grocery item not found")
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred")
