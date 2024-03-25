from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession
from data.database import get_session
from services.special_offer_service import (
    create_special_offer_service,
    get_all_special_offer_service,
    get_special_offer_service,
    update_special_offer_service,
    delete_special_offer_service,
)

from models.all_models import SpecialOffer
from schemas.special_offer import SpecialOfferCreate, SpecialOfferUpdate


router = APIRouter(prefix="/special_offers", tags=["special_offers"])


@router.post("/", response_model=SpecialOffer)
async def create_special_offer(
    special_offer_data: SpecialOfferCreate, session: AsyncSession = Depends(get_session)
) -> SpecialOffer:
    try:
        # Here, we're calling the service layer function to handle the DB operation
        # Note the name change to avoid conflicts
        new_special_offer = await create_special_offer_service(
            session, special_offer_data
        )
        return new_special_offer
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[SpecialOffer])
async def get_all_special_offers_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[SpecialOffer]:
    return await get_all_special_offer_service(session)


@router.get("/{special_offer_id}", response_model=SpecialOffer)
async def get_special_offer(
    special_offer_id: UUID, session: AsyncSession = Depends(get_session)
) -> SpecialOffer:
    special_offer = await get_special_offer_service(session, special_offer_id)
    if not special_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Special offer not found"
        )
    return special_offer


@router.put("/{special_offer_id}", response_model=SpecialOffer)
async def update_special_offer(
    special_offer_id: UUID,
    special_offer_update: SpecialOfferUpdate,
    session: AsyncSession = Depends(get_session),
) -> SpecialOffer:
    update_data_dict = special_offer_update.model_dump(exclude_unset=True)
    updated_special_offer = await update_special_offer_service(
        session, special_offer_id, update_data_dict
    )
    if not updated_special_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Special offer not found"
        )
    return updated_special_offer


@router.delete("/{special_offer_id}", status_code=204)
async def delete_special_offer(
    special_offer_id: UUID, session: AsyncSession = Depends(get_session)
):
    success = await delete_special_offer_service(session, special_offer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Special offer not found")
    return Response(status_code=204)
