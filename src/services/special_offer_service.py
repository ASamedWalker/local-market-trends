# src/services/special_offer_service.py
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.special_offer import SpecialOffer


async def create_special_offer(
    session: AsyncSession, special_offer: SpecialOffer
) -> SpecialOffer:
    try:
        session.add(special_offer)
        await session.commit()
        await session.refresh(special_offer)
        return special_offer
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_special_offer(
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


async def get_all_special_offers(session: AsyncSession) -> List[SpecialOffer]:
    try:
        result = await session.execute(select(SpecialOffer))
        special_offers = result.scalars().all()
        return special_offers
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_special_offer(
    session: AsyncSession, special_offer_id: UUID, special_offer_data: SpecialOffer
) -> Optional[SpecialOffer]:
    try:
        special_offer = await session.get(SpecialOffer, special_offer_id)
        if special_offer:
            special_offer_data.id = special_offer_id  # Ensure ID remains unchanged
            await session.merge(special_offer_data)
            await session.commit()
            return special_offer_data
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_special_offer(session: AsyncSession, special_offer_id: UUID) -> bool:
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
