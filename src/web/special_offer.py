from fastapi import APIRouter, HTTPException, Depends, status
from data.database import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID, uuid4
from services.special_offer_service import (
    create_special_offer,
    get_special_offer,
    get_all_special_offers,
    update_special_offer,
    delete_special_offer,
)


from model.special_offer import SpecialOffer

router = APIRouter(prefix="/special_offer", tags=["special_offer"])


@router.post("/", response_model=SpecialOffer)
async def create_special_offer_endpoint(
    special_offer: SpecialOffer, session: AsyncSession = Depends(get_session)
) -> SpecialOffer:
    return await create_special_offer(session, special_offer)


@router.get("/", response_model=List[SpecialOffer])
async def get_all_special_offers_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[SpecialOffer]:
    return await get_all_special_offers(session)


@router.get("/{special_offer_id}", response_model=SpecialOffer)
async def get_special_offer_endpoint(
    special_offer_id: UUID, session: AsyncSession = Depends(get_session)
) -> SpecialOffer:
    special_offer = await get_special_offer(session, special_offer_id)
    if not special_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Special offer not found"
        )
    return special_offer


@router.put("/{special_offer_id}", response_model=SpecialOffer)
async def update_special_offer_endpoint(
    special_offer_id: UUID,
    special_offer: SpecialOffer,
    session: AsyncSession = Depends(get_session),
) -> SpecialOffer:
    updated_special_offer = await update_special_offer(
        session, special_offer_id, special_offer
    )
    if not updated_special_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Special offer not found"
        )
    return updated_special_offer


@router.delete("/{special_offer_id}", response_model=SpecialOffer)
async def delete_special_offer_endpoint(
    special_offer_id: UUID, session: AsyncSession = Depends(get_session)
) -> SpecialOffer:
    special_offer = await delete_special_offer(session, special_offer_id)
    if not special_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Special offer not found"
        )
    return special_offer
