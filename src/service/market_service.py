# src/service/market_service.py
from model.grocery_item import GroceryItem
from typing import List, Optional
from uuid import UUID
import fake.market as market_db


def get_all() -> List[GroceryItem]:
    return market_db.get_all()


def get_by_name(name: str) -> Optional[GroceryItem]:
    return market_db.get_by_name(name)


def create(grocery_item: GroceryItem) -> GroceryItem:
    return market_db.create(grocery_item)


def update(item_id: UUID, grocery_item: GroceryItem) -> Optional[GroceryItem]:
    return market_db.update(item_id, grocery_item)


def delete(item_id: UUID) -> bool:
    return market_db.delete(item_id)