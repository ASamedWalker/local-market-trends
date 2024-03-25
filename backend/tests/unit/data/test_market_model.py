import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import Market


# implementing a unit test for the data layer function Market
@pytest.mark.asyncio
async def test_create_market_model():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Market.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_market = Market(
            name="Test Market",
            location_description="Test Description",
            latitude=None,
            longitude=None,
        )

        session.add(test_market)
        await session.commit()

        db_item = await session.get(Market, test_market.id)
        assert db_item is not None
        assert db_item.name == "Test Market"
        assert db_item.location_description == "Test Description"
        assert db_item.latitude is None
        assert db_item.longitude is None

    await engine.dispose()
