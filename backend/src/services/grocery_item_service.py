# src/services/grocery_item_service.py
from fastapi import HTTPException
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import select
from sqlalchemy.sql import func
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_pagination import paginate
import logging


from models.all_models import GroceryItem

logger = logging.getLogger(__name__)


async def create_grocery_item(
    session: AsyncSession, grocery_item: GroceryItem
) -> GroceryItem:
    try:
        session.add(grocery_item)
        logging.info("session has been added")
        await session.commit()
        logging.info("session has been committed")
        await session.refresh(grocery_item)
        logging.info("session has been refreshed")
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


async def get_all_grocery_items(session: AsyncSession, page: int, limit: int) -> Dict[str, Any]:
    try:
        # Get the total number of items
        count_query = select(func.count()).select_from(GroceryItem)
        total_items_result = await session.execute(count_query)
        total_items = total_items_result.scalar()

        # Get the items for the current page
        items_query = select(GroceryItem).offset((page - 1) * limit).limit(limit)
        items_result = await session.execute(items_query)
        items = items_result.scalars().all()

        # Calculate the total number of pages
        total_pages = (total_items + limit - 1) // limit

        return {
            "items": items,
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page
        }
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve all grocery items: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve all grocery items")

async def get_grocery_item_by_name(session: AsyncSession, name: str) -> Optional[GroceryItem]:
    try:
        formatted_name = name.replace('-', ' ')
        result = await session.execute(select(GroceryItem).where(func.lower(GroceryItem.name) == func.lower(formatted_name)))
        grocery_item = result.scalars().first()
        return grocery_item
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve grocery item by name: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve grocery item by name")

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


async def search_grocery_items(
    session: AsyncSession, query: str
) -> List[GroceryItem]:
    try:
        result = await session.execute(
            select(GroceryItem).where(
                GroceryItem.name.ilike(f"%{query}%")
                | GroceryItem.description.ilike(f"%{query}%")
            )
        )
        grocery_items = result.scalars().all()
        return grocery_items
    except SQLAlchemyError as e:
        logger.error(f"Failed to search grocery items: {e}")
        raise HTTPException(status_code=500, detail="Failed to search grocery items")