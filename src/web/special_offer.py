import fake.special_offer as service
from fastapi import APIRouter, HTTPException
from model.special_offer import SpecialOffer
from typing import List, Optional
from uuid import UUID, uuid4

router = APIRouter(prefix="/special_offer", tags=["special_offer"])


@router.get("/", response_model=List[SpecialOffer])
def get_all_endpoint() -> List[SpecialOffer]:
    return service.get_all()


@router.get("/{grocery_item_id}", response_model=List[SpecialOffer])
def get_by_grocery_item_id_endpoint(grocery_item_id: str) -> List[SpecialOffer]:
    return service.get_by_grocery_item_id(grocery_item_id)


@router.get("/best/{grocery_item_id}", response_model=Optional[SpecialOffer])
def get_best_offer_for_grocery_item_endpoint(
    grocery_item_id: str,
) -> Optional[SpecialOffer]:
    return service.get_best_offer_for_grocery_item(grocery_item_id)


@router.get("/active/{grocery_item_id}", response_model=List[SpecialOffer])
def get_active_offers_for_grocery_item_endpoint(
    grocery_item_id: UUID,
) -> List[SpecialOffer]:
    active_offers = service.get_active_offers()
    return [
        offer for offer in active_offers if offer.grocery_item_id == grocery_item_id
    ]


@router.post("/", response_model=SpecialOffer)
def create_endpoint(offer: SpecialOffer) -> SpecialOffer:
    return service.create(offer)


@router.put("/{offer_id}", response_model=SpecialOffer)
def update_endpoint(offer_id: str, offer: SpecialOffer) -> SpecialOffer:
    updated_offer = service.update(offer_id, offer)
    if updated_offer:
        return updated_offer
    raise HTTPException(status_code=404, detail="Offer not found")


@router.delete("/{offer_id}")
def delete_endpoint(offer_id: str) -> None:
    deleted = service.delete(offer_id)
    if deleted:
        return
    raise HTTPException(status_code=404, detail="Offer not found")
