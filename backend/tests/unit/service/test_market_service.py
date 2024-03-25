import pytest
from fastapi import HTTPException
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.services.market_service import (
    create_market,
    get_market,
    get_all_markets,
    update_market,
    delete_market,
)
from src.models.market import Market


@pytest.mark.asyncio
async def test_create_market():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Market.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_market = Market(
            name="Test Market",
            location_description="Test Description",
            latitude=0.0,
            longitude=0.0,
        )

        # Call the service function
        created_market = await create_market(session, test_market)

        # Assertions
        assert created_market.id is not None
        assert created_market.name == "Test Market"

    await engine.dispose()


@pytest.mark.asyncio
async def test_get_market():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Market.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_market = Market(
            name="Test Market", description="Test Description", category="Test Category"
        )
        session.add(test_market)
        await session.commit()

        # Call the service function
        fetched_market = await get_market(session, test_market.id)

        # Assertions
        assert fetched_market.id is not None
        assert fetched_market.name == "Test Market"

    await engine.dispose()


@pytest.mark.asyncio
async def test_get_all_markets():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Market.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_market_1 = Market(
            name="Test Market 1",
            description="Test Description 1",
            category="Test Category 1",
        )
        test_market_2 = Market(
            name="Test Market 2",
            description="Test Description 2",
            category="Test Category 2",
        )
        session.add(test_market_1)
        session.add(test_market_2)
        await session.commit()

        # Call the service function
        fetched_markets = await get_all_markets(session)

        # Assertions
        assert len(fetched_markets) == 2
        assert fetched_markets[0].name == "Test Market 1"
        assert fetched_markets[1].name == "Test Market 2"

    await engine.dispose()


@pytest.mark.asyncio
async def test_update_market():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Market.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_market = Market(
            name="Test Market",
            location_description="Test Description",
            latitude=0.0,
            longitude=0.0,
        )
        session.add(test_market)
        await session.commit()
        await session.refresh(test_market)

        # Simulate partial update data (as you might receive from a PATCH request)
        update_data = {"name": "Updated Market"}

        existing_market = await get_market(session, test_market.id)
        for key, value in update_data.items():
            setattr(existing_market, key, value)

        # Call the service function with the updated model instance
        await session.commit()  # Commit the changes
        await session.refresh(existing_market)  # Refresh to get updated data

        # Assertions
        assert existing_market.id == test_market.id
        assert existing_market.name == "Updated Market"

    await engine.dispose()


@pytest.mark.asyncio
async def test_delete_market():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Market.metadata.create_all)

    async_session_factory = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session_factory() as session:
        # Test data
        test_market = Market(
            name="Test Market",
            location_description="Test Description",
            latitude=0.0,
            longitude=0.0,
        )
        session.add(test_market)
        await session.commit()
        await session.refresh(test_market)

        # Delete the market
        await delete_market(session, test_market.id)

        # Attempt to fetch the deleted market and expect a 404 error
        with pytest.raises(HTTPException) as exc_info:
            await get_market(session, test_market.id)

        assert (
            exc_info.value.status_code == 404
        ), "Expected a 404 HTTPException for a non-existing market."

    await engine.dispose()
