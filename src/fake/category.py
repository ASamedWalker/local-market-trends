from model.category import Category
from uuid import UUID, uuid4


# fake data, replaced with real database and SQLModel
# Fake categories
_categories = [
    Category(
        id=uuid4(), name="Electronics", description="Gadgets and electronic devices."
    ),
    Category(id=uuid4(), name="Furniture", description="Home and office furniture."),
]


def get_all() -> list[Category]:
    return _categories


def get_one(name: str) -> Category:
    for category in _categories:
        if category.name == name:
            return category
    return None


def create(category: Category) -> Category:
    return category


def update(name: str, category: Category) -> Category:
    for i, c in enumerate(_categories):
        if c.name == name:
            _categories[i] = category
            return category
    return None


def delete(name: str) -> Category:
    for i, c in enumerate(_categories):
        if c.name == name:
            return _categories.pop(i)
    return None


