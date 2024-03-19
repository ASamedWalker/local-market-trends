import pytest
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.services.special_offer_service import create_special_offer
from src.models.special_offer import SpecialOffer
from src.models.grocery_item import GroceryItem


@pytest.mark.asyncio
async def test_create_special_offer():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        # Create all tables in the in-memory database for the test context
        await conn.run_sync(SpecialOffer.metadata.create_all)
        await conn.run_sync(GroceryItem.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data preparation
        test_grocery_item = GroceryItem(
            name="Test Item", description="Test Description", category="Test Category"
        )
        session.add(test_grocery_item)
        await session.commit()

        test_special_offer = SpecialOffer(
            grocery_item_id=test_grocery_item.id,
            description="Test Special Offer",
            valid_from=datetime.utcnow(),
            valid_to=datetime.utcnow(),
        )

        # Call the service function with the test session and special offer
        created_special_offer = await create_special_offer(session, test_special_offer)

        # Assertions to validate the creation of the special offer
        assert created_special_offer.id is not None
        assert created_special_offer.description == "Test Special Offer"

    # Clean-up
    await engine.dispose()
