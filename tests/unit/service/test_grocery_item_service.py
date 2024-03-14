import pytest
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.services.grocery_item_service import (
    create_grocery_item,
    get_grocery_item,
    get_all_grocery_items,
    update_grocery_item,
    delete_grocery_item,
)
from src.models.grocery_item import GroceryItem


@pytest.mark.asyncio
async def test_create_grocery_item():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(GroceryItem.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_grocery_item = GroceryItem(
            name="Test Item", description="Test Description", category="Test Category"
        )

        # Call the service function
        created_item = await create_grocery_item(session, test_grocery_item)

        # Assertions
        assert created_item.id is not None
        assert created_item.name == "Test Item"

    await engine.dispose()


@pytest.mark.asyncio
async def test_get_grocery_item():
    # Setup test database and session
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

        # Call the service function
        fetched_item = await get_grocery_item(session, test_grocery_item.id)

        # Assertions
        assert fetched_item.id is not None
        assert fetched_item.name == "Test Item"

    await engine.dispose()


@pytest.mark.asyncio
async def test_get_all_grocery_items():
    # Setup test database and session
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(GroceryItem.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        # Test data
        test_grocery_item_1 = GroceryItem(
            name="Test Item 1",
            description="Test Description 1",
            category="Test Category 1",
        )
        test_grocery_item_2 = GroceryItem(
            name="Test Item 2",
            description="Test Description 2",
            category="Test Category 2",
        )
        session.add(test_grocery_item_1)
        session.add(test_grocery_item_2)
        await session.commit()

        # Call the service function
        fetched_items = await get_all_grocery_items(session)

        # Assertions
        assert len(fetched_items) == 2
        assert fetched_items[0].name == "Test Item 1"
        assert fetched_items[1].name == "Test Item 2"

    await engine.dispose()


@pytest.mark.asyncio
async def test_update_grocery_item():
    # Setup test database and session
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

        # Call the service function
        updated_item = await update_grocery_item(
            session, test_grocery_item.id, GroceryItem(name="Updated Item")
        )

        # Assertions
        assert updated_item.id is not None
        assert updated_item.name == "Updated Item"

    await engine.dispose()


@pytest.mark.asyncio
async def test_delete_grocery_item():
    # Setup test database and session
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

        # Call the service function
        deleted_item = await delete_grocery_item(session, test_grocery_item.id)

        # Assertions
        assert deleted_item.id is not None
        assert deleted_item.name == "Test Item"

    await engine.dispose()
