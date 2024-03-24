import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import SpecialOffer
from uuid import UUID, uuid4
from datetime import datetime


# implementing a unit test for the data layer function SpecialOffer
@pytest.mark.asyncio
async def test_create_special_offer_model():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SpecialOffer.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_special_offer = SpecialOffer(
            grocery_item_id=str(uuid4()),
            description="Test Description",
            valid_from=datetime.utcnow(),
            valid_to=datetime.utcnow(),
        )

        session.add(test_special_offer)
        await session.commit()

        db_item = await session.get(SpecialOffer, test_special_offer.id)
        assert db_item is not None
        assert db_item.grocery_item_id == test_special_offer.grocery_item_id
        assert db_item.description == "Test Description"
        assert db_item.valid_from == test_special_offer.valid_from
        assert db_item.valid_to == test_special_offer.valid_to

    await engine.dispose()
