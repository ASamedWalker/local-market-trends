from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from models.category import Category
from fake.category import service


router = APIRouter(prefix="/category")


@router.get("/", response_model=List[Category])
def get_all_category() -> List[Category]:
    return service.get_all()


@router.get("/{name}", response_model=Category)
def get_one_category(name: str) -> Category | None:
    result = service.get_one(name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Category not found")


@router.post("/", response_model=Category)
def create_category(category: Category) -> Category:
    try:
        new_category = service.create(category)
        return new_category
    except Exception as e:
        # Log the error or send it back as part of the response
        raise HTTPException(status_code=500, detail=f"Failed to create category: {e}")


@router.put("/{name}", response_model=Category)
def update_category(name: str, category: Category) -> Category:
    try:
        return service.update(name, category)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{name}", response_model=Category)
def delete_category(name: str) -> Category:
    try:
        return service.delete(name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
