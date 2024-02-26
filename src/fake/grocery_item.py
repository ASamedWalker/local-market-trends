# Creating a fake grocery item  data for unit testing
from model.grocery_item import GroceryItem
from uuid import uuid4, UUID
from typing import List, Optional

_grocery_items: List[GroceryItem] = [
    GroceryItem(
        id=uuid4(), name="Apple", description="A sweet, edible fruit", category="Fruits"
    ),
    GroceryItem(
        id=uuid4(), name="Banana", description="A long curved fruit", category="Fruits"
    ),
    GroceryItem(
        id=uuid4(),
        name="Spinach",
        description="A green leafy vegetable",
        category="Vegetables",
    ),
    GroceryItem(
        id=uuid4(),
        name="Carrot",
        description="A root vegetable, usually orange",
        category="Vegetables",
    ),
]


def get_all() -> list[GroceryItem]:
    return _grocery_items


def get_by_name(name: str) -> GroceryItem:
    for item in _grocery_items:
        if item.name.lower() == name.lower():
            return item
    return None


def create(grocery_item: GroceryItem) -> GroceryItem:
    _grocery_items.append(grocery_item)
    return grocery_item


def update(id: UUID, updated_item: GroceryItem) -> Optional[GroceryItem]:
    for item in _grocery_items:
        if item.id == id:
            item.name = updated_item.name
            item.description = updated_item.description
            item.category = updated_item.category
            return item
    return None


def delete(item_id: UUID) -> Optional[GroceryItem]:
    for i, item in enumerate(_grocery_items):
        if item.id == item_id:
            return _grocery_items.pop(i)
    return None
