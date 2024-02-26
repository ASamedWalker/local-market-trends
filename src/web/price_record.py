from fastapi import APIRouter, HTTPException
from model.price_record import PriceRecord
import fake.price_record as service
from typing import Optional, List


router = APIRouter(prefix="/price_record", tags=["price_record"])


@router.get("/", response_model=List[PriceRecord])
def get_all_endpoint() -> List[PriceRecord]:
    return service.get_all()


@router.get("/{grocery_item_id}", response_model=List[PriceRecord])
def get_by_grocery_item_id_endpoint(grocery_item_id: str) -> List[PriceRecord]:
    return service.get_by_grocery_item_id(grocery_item_id)


@router.post("/", response_model=PriceRecord)
def create_endpoint(record: PriceRecord) -> PriceRecord:
    return service.create(record)


@router.put("/{record_id}", response_model=PriceRecord)
def update_endpoint(record_id: str, record: PriceRecord) -> PriceRecord:
    updated_record = service.update(record_id, record)
    if updated_record:
        return updated_record
    raise HTTPException(status_code=404, detail="Record not found")


@router.delete("/{record_id}")
def delete_endpoint(record_id: str) -> None:
    deleted = service.delete(record_id)
    if deleted:
        return
    raise HTTPException(status_code=404, detail="Record not found")
