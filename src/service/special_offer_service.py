# src/services/special_offer_service.py

from typing import List, Optional
from uuid import UUID
import fake.special_offer as special_offer_db
from model.special_offer import SpecialOffer


def get_all_special_offers() -> List[SpecialOffer]:
    """Retrieve all special offers."""
    return special_offer_db.get_all()


def get_special_offer_by_id(offer_id: UUID) -> Optional[SpecialOffer]:
    """Retrieve a special offer by its ID."""
    return special_offer_db.get_by_id(offer_id)


def get_active_special_offers() -> List[SpecialOffer]:
    """Retrieve all active special offers."""
    return special_offer_db.get_active_offers()


def get_best_offer_for_grocery_item(grocery_item_id: UUID) -> Optional[SpecialOffer]:
    """Retrieve the best offer for a given grocery item."""
    return special_offer_db.get_best_offer_for_grocery_item(grocery_item_id)


def create_special_offer(special_offer: SpecialOffer) -> SpecialOffer:
    """Create a new special offer."""
    return special_offer_db.create(special_offer)


def update_special_offer(
    offer_id: UUID, updated_offer: SpecialOffer
) -> Optional[SpecialOffer]:
    """Update an existing special offer."""
    return special_offer_db.update(offer_id, updated_offer)


def delete_special_offer(offer_id: UUID) -> bool:
    """Delete a special offer."""
    deleted_offer = special_offer_db.delete(offer_id)
    return deleted_offer is not None


def log_special_offer_usage(offer_id: UUID):
    """Log usage of a special offer."""
    special_offer_db.log_offer_usage(offer_id)
