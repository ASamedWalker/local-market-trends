from model.location import Location
import fake.location as data
from typing import List


def get_all() -> List[Location]:
    return data.get_all()


def get_one(name: str) -> Location | None:
    return data.get_one(name)


def create(location: Location) -> Location:
    return data.create(location)


def update(name: str, updated_location: Location) -> Location | None:
    return data.update(name, updated_location)


def delete(name: str) -> Location | None:
    return data.delete(name)
