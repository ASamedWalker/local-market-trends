from model.location import Location
from uuid import UUID, uuid4


# fake data, replaced with real database and SQLModel
# Fake locations
_locations = [
    Location(id=uuid4(), city="New York", state="NY", country="USA"),
    Location(id=uuid4(), city="San Francisco", state="CA", country="USA"),
]


def get_all() -> list[Location]:
    return _locations


def get_one(city: str) -> Location:
    for location in _locations:
        if location.city == city:
            return location
    return None


def create(location: Location) -> Location:
    return location


def update(city: str, location: Location) -> Location:
    for i, l in enumerate(_locations):
        if l.city == city:
            _locations[i] = location
            return location
    return None


def delete(city: str) -> Location:
    for i, l in enumerate(_locations):
        if l.city == city:
            return _locations.pop(i)
    return None
