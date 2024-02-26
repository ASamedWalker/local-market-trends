from fastapi import APIRouter, HTTPException
from uuid import UUID
from model.grocery_item import GroceryItem
import fake.grocery_item as service
from typing import Optional, List


router = APIRouter(prefix="/grocery_item", tags=["grocery_item"])


@router.get("/", response_model=List[GroceryItem])
def get_all_endpoint() -> List[GroceryItem]:
    return service.get_all()


@router.get("/{name}", response_model=GroceryItem)
def get_by_name_endpoint(name: str) -> GroceryItem:
    item = service.get_by_name(name)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", response_model=GroceryItem)
def create_endpoint(item: GroceryItem) -> GroceryItem:
    return service.create(item)


@router.put("/{id}", response_model=GroceryItem)
def update_endpoint(id: UUID, item: GroceryItem) -> GroceryItem:
    updated_item = service.update(id, item)
    if updated_item:
        return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{id}")
def delete_endpoint(id: UUID) -> None:
    deleted = service.delete(id)
    if deleted:
        return
    raise HTTPException(status_code=404, detail="Item not found")
