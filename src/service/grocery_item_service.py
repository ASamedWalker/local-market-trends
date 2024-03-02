# src/services/grocery_item_service.py
from typing import List, Optional
from uuid import UUID
import fake.grocery_item as grocery_item_db
from model.grocery_item import GroceryItem


def get_all_grocery_items() -> List[GroceryItem]:
    return grocery_item_db.get_all()


def get_grocery_item_by_id(item_id: UUID) -> Optional[GroceryItem]:
    return grocery_item_db.get_by_id(item_id)


def create_grocery_item(grocery_item: GroceryItem) -> GroceryItem:
    return grocery_item_db.create(grocery_item)


def update_grocery_item(
    item_id: UUID, grocery_item: GroceryItem
) -> Optional[GroceryItem]:
    return grocery_item_db.update(item_id, grocery_item)


def delete_grocery_item(item_id: UUID) -> bool:
    return grocery_item_db.delete(item_id)
