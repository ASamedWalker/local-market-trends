from model.special_offer import SpecialOffer
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID, uuid4


_special_offers: List[SpecialOffer] = [
    SpecialOffer(
        id=uuid4(),
        grocery_item_id=uuid4(),
        description="Buy one get one free",
        valid_from=date(2021, 1, 1),
        valid_to=date(2021, 12, 31),
    ),
    SpecialOffer(
        id=uuid4(),
        grocery_item_id=uuid4(),
        description="25% off",
        valid_from=date(2021, 1, 1),
        valid_to=date(2021, 12, 31),
    ),
    SpecialOffer(
        id=uuid4(),
        grocery_item_id=uuid4(),
        description="3 for 2",
        valid_from=date(2021, 1, 1),
        valid_to=date(2021, 12, 31),
    ),
]


def get_all() -> list[SpecialOffer]:
    return _special_offers


def get_by_id(id: UUID) -> SpecialOffer:
    for offer in _special_offers:
        if offer.id == id:
            return offer
    return None


def get_best_offer_for_grocery_item(grocery_item_id: UUID) -> Optional[SpecialOffer]:
    offers = [
        offer
        for offer in _special_offers
        if offer.grocery_item_id == grocery_item_id and offer.is_valid_offer()
    ]
    if not offers:
        return None
    # Simplified logic: Assumes the last valid offer is the best
    # Implement your own logic to decide which offer is the best
    return sorted(offers, key=lambda x: x.valid_to, reverse=True)[0]


def log_offer_usage(offer_id: UUID):
    # Dummy function to demonstrate logging offer usage
    # In a real app, you might log this to a database or analytics service
    print(f"Offer {offer_id} was used at {datetime.now()}")


def get_active_offers() -> list[SpecialOffer]:
    """Returns active offers based on the current date."""
    current_date = datetime.utcnow()
    return [
        offer
        for offer in _special_offers
        if offer.valid_from <= current_date <= offer.valid_to
    ]


def create(special_offer: SpecialOffer) -> SpecialOffer:
    _special_offers.append(special_offer)
    return special_offer


def update(id: UUID, updated_offer: SpecialOffer) -> Optional[SpecialOffer]:
    for offer in _special_offers:
        if offer.id == id:
            offer.description = updated_offer.description
            offer.valid_from = updated_offer.valid_from
            offer.valid_to = updated_offer.valid_to
            return offer
    return None


def delete(offer_id: UUID) -> Optional[SpecialOffer]:
    for i, offer in enumerate(_special_offers):
        if offer.id == offer_id:
            return _special_offers.pop(i)
    return None
