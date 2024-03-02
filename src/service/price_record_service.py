# src/service/price_record_service.py
import fake.price_record as price_record_db
from model.price_record import PriceRecord
from typing import List, Optional
from uuid import UUID


def get_all() -> List[PriceRecord]:
    return price_record_db.get_all()


def get_by_grocery_item_id(grocery_item_id: str) -> List[PriceRecord]:
    return price_record_db.get_by_grocery_item_id(grocery_item_id)


def create(price_record: PriceRecord) -> PriceRecord:
    return price_record_db.create(price_record)


def update(price_record_id: UUID, price_record: PriceRecord) -> PriceRecord:
    return price_record_db.update(price_record_id, price_record)


def delete(price_record_id: UUID) -> bool:
    return price_record_db.delete(price_record_id)
