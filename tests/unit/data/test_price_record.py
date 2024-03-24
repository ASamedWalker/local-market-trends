import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import PriceRecord
from uuid import UUID, uuid4
from datetime import datetime


# implementing a unit test for the data layer function PriceRecord
@pytest.mark.asyncio
async def test_create_price_record_model():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(PriceRecord.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_price_record = PriceRecord(
            grocery_item_id=str(uuid4()),
            market_id=str(uuid4()),
            price=10.0,
            date_recorded=datetime.utcnow(),
        )

        session.add(test_price_record)
        await session.commit()

        db_item = await session.get(PriceRecord, test_price_record.id)
        assert db_item is not None
        assert db_item.grocery_item_id == test_price_record.grocery_item_id
        assert db_item.market_id == test_price_record.market_id
        assert db_item.price == 10.0
        assert db_item.date_recorded == test_price_record.date_recorded

    await engine.dispose()
