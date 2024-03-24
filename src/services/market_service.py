# src/service/market_service.py
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

# import fake.market as market_db

from src.models.all_models import Market


async def create_market(session: AsyncSession, market: Market) -> Market:
    try:
        session.add(market)
        await session.commit()
        await session.refresh(market)
        return market
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Could not create market due to integrity error: {str(e)}",
        )
    except SQLAlchemyError as e:  # A more general error catch
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_market(session: AsyncSession, market_id: UUID) -> Optional[Market]:
    try:
        result = await session.get(Market, market_id)
        if not result:
            raise HTTPException(status_code=404, detail="Market not found")
        return result
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_markets(session: AsyncSession) -> List[Market]:
    try:
        result = await session.execute(select(Market))
        markets = result.scalars().all()
        return markets
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_market(
    session: AsyncSession, market_id: UUID, market_data: Market
) -> Optional[Market]:
    try:
        market = await session.get(Market, market_id)
        if market:
            market_data.id = market.id  # Ensure ID is not changed
            await session.merge(market_data)
            await session.commit()
            return market_data
        else:
            raise HTTPException(status_code=404, detail="Market not found")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_market(session: AsyncSession, market_id: UUID) -> bool:
    try:
        market = await session.get(Market, market_id)
        if market:
            await session.delete(market)
            await session.commit()
            return market
        else:
            raise HTTPException(status_code=404, detail="Market not found")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
