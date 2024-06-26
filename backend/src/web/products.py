from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_sqla import setup, Paginate, Session, Page
from typing import List, Dict, Any
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from data.database import get_session
from services.grocery_item_service import (
    create_grocery_item,
    get_grocery_item,
    get_all_grocery_items,
    get_grocery_item_by_name,
    update_grocery_item,
    delete_grocery_item,
    search_grocery_items,
)
from models.all_models import GroceryItem

# Create a new router for products
router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=GroceryItem)
async def create_product_endpoint(
    product: GroceryItem, session: AsyncSession = Depends(get_session)
) -> GroceryItem:
    return await create_grocery_item(session, product)

@router.get("/", response_model=Dict[str, Any])
async def get_all_products_endpoint(
    session: AsyncSession = Depends(get_session),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    pagination_result = await get_all_grocery_items(session, page, limit)
    return pagination_result

@router.get("/{product_name}", response_model=GroceryItem)
async def get_product_endpoint(
    product_name: str, session: AsyncSession = Depends(get_session)
) -> GroceryItem:
    print(f"Requested product_name: {product_name}")
    product = await get_grocery_item_by_name(session, product_name)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=GroceryItem)
async def update_product_endpoint(
    product_id: UUID,
    product: GroceryItem,
    session: AsyncSession = Depends(get_session),
) -> GroceryItem:
    product_dict = product.model_dump()

    updated_product = await update_grocery_item(
        session, product_id, product_dict
    )
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated_product

@router.delete("/{product_id}", response_model=GroceryItem)
async def delete_product_endpoint(
    product_id: UUID, session: AsyncSession = Depends(get_session)
) -> GroceryItem:
    product = await get_grocery_item(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    await delete_grocery_item(session, product_id)
    return product

@router.get("/search/{product_name}", response_model=List[GroceryItem])
async def search_product_items(product_name: str, session: AsyncSession = Depends(get_session)):
    items = await search_grocery_items(session, product_name)
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items