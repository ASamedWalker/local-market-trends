# src/services/special_offer_service.py
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.special_offer import SpecialOffer
from src.schemas.special_offer import SpecialOfferCreate, SpecialOfferUpdate


async def create_special_offer_service(
    session: AsyncSession, special_offer: SpecialOfferCreate
) -> SpecialOffer:
    try:
        new_special_offer = SpecialOffer(**special_offer.model_dump())
        session.add(new_special_offer)
        await session.commit()
        await session.refresh(new_special_offer)
        return new_special_offer
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_special_offer_service(
    session: AsyncSession, special_offer_id: UUID
) -> Optional[SpecialOffer]:
    try:
        result = await session.get(SpecialOffer, special_offer_id)
        if not result:
            raise HTTPException(status_code=404, detail="Special offer not found")
        return result
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_special_offer_service(session: AsyncSession) -> List[SpecialOffer]:
    try:
        result = await session.execute(select(SpecialOffer))
        special_offers = result.scalars().all()
        return special_offers
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_special_offer_service(
    session: AsyncSession,
    special_offer_id: UUID,
    special_offer_update_data: dict,
) -> Optional[SpecialOffer]:
    try:
        special_offer = await session.get(SpecialOffer, special_offer_id)
        if not special_offer:
            raise HTTPException(status_code=404, detail="Special offer not found")

        update_data_dict = special_offer_update_data
        for key, value in update_data_dict.items():
            if hasattr(special_offer, key):
                setattr(special_offer, key, value)

        await session.commit()
        await session.refresh(special_offer)
        return special_offer
    except NoResultFound as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Special offer not found")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_special_offer_service(
    session: AsyncSession, special_offer_id: UUID
) -> bool:
    try:
        special_offer = await session.get(SpecialOffer, special_offer_id)
        if special_offer:
            await session.delete(special_offer)
            await session.commit()
            return True
        else:
            return False
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
