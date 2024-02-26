from fastapi import APIRouter, HTTPException
from model.listing import Listing
import fake.listing as service
from typing import List, Optional


router = APIRouter(prefix="/listing")


@router.get("/", response_model=List[Listing])
def get_all_listing() -> List[Listing]:
    return service.get_all()


@router.get("/{title}", response_model=Listing)
def get_one_listing(title: str) -> Listing | None:
    result = service.get_one(title)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Listing not found")


@router.post("/", response_model=Listing)
def create_listing(listing: Listing) -> Listing:
    try:
        new_listing = service.create(listing)
        return new_listing
    except Exception as e:
        # Log the error or send it back as part of the response
        raise HTTPException(status_code=500, detail=f"Failed to create listing: {e}")


@router.put("/{title}", response_model=Listing)
def update_listing(title: str, listing: Listing) -> Listing:
    try:
        return service.update(title, listing)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{title}", response_model=Listing)
def delete_listing(title: str) -> Listing | None:
    return service.delete(title)
