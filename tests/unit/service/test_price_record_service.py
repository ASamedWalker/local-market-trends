import pytest
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.services.price_record_service import create_price_record
from src.models.price_record import PriceRecord
from src.models.grocery_item import GroceryItem
from src.models.market import Market


@pytest.mark.asyncio
async def test_create_price_record():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        # Create all tables in the in-memory database for the test context
        await conn.run_sync(PriceRecord.metadata.create_all)
        await conn.run_sync(GroceryItem.metadata.create_all)
        await conn.run_sync(Market.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Creating a test session
    async with async_session() as session:
        # Test data preparation
        test_market = Market(name="Test Market", location_description="Test Location")
        test_grocery_item = GroceryItem(
            name="Test Item", description="Test Description", category="Test Category"
        )
        session.add(test_market)
        session.add(test_grocery_item)
        await session.commit()

        test_price_record = PriceRecord(
            grocery_item_id=test_grocery_item.id,
            market_id=test_market.id,
            price=100.0,
            date_recorded=datetime.utcnow(),
        )

        # Call the service function with the test session and price record
        created_price_record = await create_price_record(session, test_price_record)

        # Assertions to validate the creation of the price record
        assert created_price_record.id is not None
        assert created_price_record.price == 100.0

    # Clean-up
    await engine.dispose()
