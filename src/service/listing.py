# Creating service layer in order to talk between the web and the fake layer
# Sole responsibility of the service layer is what goes into and out of the data/fake layer
from model.listing import Listing
import fake.listing as data
from typing import List


def get_all() -> List[Listing]:
    return data.get_all()


def get_one(title: str) -> Listing | None:
    return data.get_one(title)


def create(listing: Listing) -> Listing:
    return data.create(listing)


def update(title: str, updated_listing: Listing) -> Listing | None:
    return data.update(title, updated_listing)


def delete(title: str) -> Listing | None:
    return data.delete(title)
