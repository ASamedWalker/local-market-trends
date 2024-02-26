from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from models.location import Location
from fake.location import service


router = APIRouter(prefix="/location")


@router.get("/", response_model=List[Location])
def get_all_location() -> List[Location]:
    return service.get_all()


@router.get("/{name}", response_model=Location)
def get_one_location(name: str) -> Location | None:
    result = service.get_one(name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Location not found")


@router.post("/", response_model=Location)
def create_location(location: Location) -> Location:
    try:
        new_location = service.create(location)
        return new_location
    except Exception as e:
        # Log the error or send it back as part of the response
        raise HTTPException(status_code=500, detail=f"Failed to create location: {e}")


@router.put("/{name}", response_model=Location)
def update_location(name: str, location: Location) -> Location:
    try:
        return service.update(name, location)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{name}", response_model=Location)
def delete_location(name: str) -> Location:
    try:
        return service.delete(name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
