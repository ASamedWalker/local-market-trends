import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import GroceryItem


# implementing a unit test for the data layer function Gr
@pytest.mark.asyncio
async def test_create_grocery_item_model():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(GroceryItem.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_grocery_item = GroceryItem(
            name="Test Item", description="Test Description", category="Test Category"
        )

        session.add(test_grocery_item)
        await session.commit()

        db_item = await session.get(
            GroceryItem, test_grocery_item.id
        )  # Await the retrieval
        assert db_item is not None
        assert db_item.name == "Test Item"  # Use the same data as what you've added
        assert db_item.description == "Test Description"
        assert db_item.category == "Test Category"  # Verify the

    await engine.dispose()
