from model.category import Category
import fake.category as data
from typing import List


def get_all() -> List[Category]:
    return data.get_all()


def get_one(name: str) -> Category | None:
    return data.get_one(name)


def create(category: Category) -> Category:
    return data.create(category)


def update(name: str, updated_category: Category) -> Category | None:
    return data.update(name, updated_category)


def delete(name: str) -> Category | None:
    return data.delete(name)
