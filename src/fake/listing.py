from fastapi import HTTPException
from model.listing import Listing
from uuid import UUID, uuid4
from typing import Optional

# fake data, replaced with real database and SQLModel
# Fake listings
_listings = [
    Listing(
        id=uuid4(),
        title="MacBook Pro 16 inch",
        description="2021 Model, 16GB RAM, 512GB SSD, M1 Pro chip.",
        price=2400.0,
        category_id=uuid4(),
        location_id=uuid4(),
    ),
    Listing(
        id=uuid4(),
        title="Ergonomic Office Chair",
        description="Mesh back, adjustable height, lumbar support.",
        price=150.0,
        category_id=uuid4(),
        location_id=uuid4(),
    ),
]


def get_all() -> list[Listing]:
    return _listings


def get_one(title: str) -> Listing:
    for listing in _listings:
        if listing.title == title:
            return listing
    return None


# The following are nonfunctional for now,
# so they just act like they work, without modifying
# the actual fake _creatures list:
def create(listing: Listing) -> Listing:
    _listings.append(listing)
    print(_listings)
    return listing


def update(title: str, updated_listing: Listing) -> Optional[Listing]:
    for i, listing in enumerate(_listings):
        if listing.title == title:
            _listings[i] = updated_listing
            return _listings[i]
    raise HTTPException(status_code=404, detail="Listing not found")


def delete(title: str) -> Optional[Listing]:
    for i, listing in enumerate(_listings):
        if listing.title == title:
            return _listings.pop(i)
    return None
