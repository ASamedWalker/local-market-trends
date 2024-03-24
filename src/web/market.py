from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional, List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from src.data.database import get_session
from src.services.market_service import (
    create_market,
    get_market,
    get_all_markets,
    update_market,
    delete_market,
)


from src.models.all_models import Market

router = APIRouter(prefix="/market", tags=["market"])


@router.post("/", response_model=Market)
async def create_market_endpoint(
    market: Market, session: AsyncSession = Depends(get_session)
) -> Market:
    return await create_market(session, market)


@router.get("/", response_model=List[Market])
async def get_all_markets_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[Market]:
    return await get_all_markets(session)


@router.get("/{market_id}", response_model=Market)
async def get_market_endpoint(
    market_id: UUID, session: AsyncSession = Depends(get_session)
) -> Market:
    market = await get_market(session, market_id)
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Market not found"
        )
    return market


@router.put("/{market_id}", response_model=Market)
async def update_market_endpoint(
    market_id: UUID,
    market: Market,
    session: AsyncSession = Depends(get_session),
) -> Market:
    updated_market = await update_market(session, market_id, market)
    if not updated_market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Market not found"
        )
    return updated_market


@router.delete("/{market_id}", response_model=Market)
async def delete_market_endpoint(
    market_id: UUID, session: AsyncSession = Depends(get_session)
) -> Market:
    deleted_market = await delete_market(session, market_id)
    if not deleted_market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Market not found"
        )
    return deleted_market
