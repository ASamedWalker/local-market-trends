# src/service/price_record_service.py
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID


from models.all_models import PriceRecord


async def create_price_record(
    session: AsyncSession, price_record: PriceRecord
) -> PriceRecord:
    try:
        session.add(price_record)
        await session.commit()
        await session.refresh(price_record)
        return price_record
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_price_record(
    session: AsyncSession, price_record_id: UUID
) -> Optional[PriceRecord]:
    try:
        result = await session.get(PriceRecord, price_record_id)
        if not result:
            raise HTTPException(status_code=404, detail="Price record not found")
        return result
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_price_records(session: AsyncSession) -> List[PriceRecord]:
    try:
        result = await session.execute(select(PriceRecord))
        price_records = result.scalars().all()
        return price_records
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_price_record(
    session: AsyncSession, price_record_id: UUID, price_record_data: PriceRecord
) -> Optional[PriceRecord]:
    try:
        price_record = await session.get(PriceRecord, price_record_id)
        if price_record:
            price_record_data.id = price_record_id  # Ensure ID remains unchanged
            await session.merge(price_record_data)
            await session.commit()
            return price_record_data
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_price_record(
    session: AsyncSession, price_record_id: UUID
) -> Optional[PriceRecord]:
    try:
        price_record = await session.get(PriceRecord, price_record_id)
        if price_record:
            await session.delete(price_record)
            await session.commit()
            return price_record
        else:
            raise HTTPException(status_code=404, detail="Price record not found")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
