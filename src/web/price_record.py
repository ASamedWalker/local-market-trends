from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from data.database import get_session
from services.price_record_service import (
    create_price_record,
    get_price_record,
    get_all_price_records,
    update_price_record,
    delete_price_record,
)
from uuid import UUID
from typing import Optional, List


from model.price_record import PriceRecord


router = APIRouter(prefix="/price_record", tags=["price_record"])


@router.post("/", response_model=PriceRecord)
async def create_price_record_endpoint(
    price_record: PriceRecord, session: AsyncSession = Depends(get_session)
) -> PriceRecord:
    return await create_price_record(session, price_record)


@router.get("/", response_model=List[PriceRecord])
async def get_all_price_records_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[PriceRecord]:
    return await get_all_price_records(session)


@router.get("/{price_record_id}", response_model=PriceRecord)
async def get_price_record_endpoint(
    price_record_id: UUID, session: AsyncSession = Depends(get_session)
) -> PriceRecord:
    price_record = await get_price_record(session, price_record_id)
    if not price_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Price record not found"
        )
    return price_record


@router.put("/{price_record_id}", response_model=PriceRecord)
async def update_price_record_endpoint(
    price_record_id: UUID,
    price_record: PriceRecord,
    session: AsyncSession = Depends(get_session),
) -> PriceRecord:
    updated_price_record = await update_price_record(
        session, price_record_id, price_record
    )
    if not updated_price_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Price record not found"
        )
    return updated_price_record


@router.delete("/{price_record_id}", response_model=PriceRecord)
async def delete_price_record_endpoint(
    price_record_id: UUID, session: AsyncSession = Depends(get_session)
) -> PriceRecord:
    deleted_price_record = await delete_price_record(session, price_record_id)
    if not deleted_price_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Price record not found"
        )
    return deleted_price_record
