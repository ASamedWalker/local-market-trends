# Creating a fake grocery item  data for unit testing
from model.grocery_item import GroceryItem
from uuid import uuid4

grocery_items = [
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
    return grocery_items


def get_by_name(name: str) -> GroceryItem:
    for item in grocery_items:
        if item.name.lower() == name.lower():
            return item
    return None


def create(grocery_item: GroceryItem) -> GroceryItem:
    grocery_item.id = uuid4()
    grocery_items.append(grocery_item)
    return grocery_item


def update(name: str, updated_item: GroceryItem) -> GroceryItem:
    for i, item in enumerate(grocery_items):
        if item.id == updated_item.id:
            grocery_items[i] = updated_item
            return updated_item
    return None


def delete(name: str) -> GroceryItem:
    for i, item in enumerate(grocery_items):
        if item.name.lower() == name.lower():
            del grocery_items[i]
            return True
    return False
