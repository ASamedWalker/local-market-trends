import pytest
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.services.special_offer_service import (
    create_special_offer,
    get_special_offer,
    get_all_special_offers,
    update_special_offer,
    delete_special_offer,
)
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


@pytest.mark.asyncio
async def test_get_special_offer():
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
        session.add(test_special_offer)
        await session.commit()

        # Call the service function with the test session and special offer
        fetched_special_offer = await get_special_offer(session, test_special_offer.id)

        # Assertions to validate the fetched special offer
        assert fetched_special_offer.id is not None
        assert fetched_special_offer.description == "Test Special Offer"

    # Clean-up
    await engine.dispose()


@pytest.mark.asyncio
async def test_get_all_special_offers():
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

        test_special_offer_1 = SpecialOffer(
            grocery_item_id=test_grocery_item.id,
            description="Test Special Offer 1",
            valid_from=datetime.utcnow(),
            valid_to=datetime.utcnow(),
        )
        test_special_offer_2 = SpecialOffer(
            grocery_item_id=test_grocery_item.id,
            description="Test Special Offer 2",
            valid_from=datetime.utcnow(),
            valid_to=datetime.utcnow(),
        )
        session.add(test_special_offer_1)
        session.add(test_special_offer_2)
        await session.commit()

        # Call the service function with the test session
        fetched_special_offers = await get_all_special_offers(session)

        # Assertions to validate the fetched special offers
        assert len(fetched_special_offers) == 2

    # Clean-up
    await engine.dispose()


@pytest.mark.asyncio
async def test_update_special_offer():
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
        session.add(test_special_offer)
        await session.commit()

        # Call the service function with the test session and special offer
        updated_special_offer = await update_special_offer(
            session, test_special_offer.id, test_special_offer
        )

        # Assertions to validate the updated special offer
        assert updated_special_offer.id is not None
        assert updated_special_offer.description == "Test Special Offer"

    # Clean-up
    await engine.dispose()


@pytest.mark.asyncio
async def test_delete_special_offer():
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
        session.add(test_special_offer)
        await session.commit()

        # Call the service function with the test session and special offer
        is_deleted = await delete_special_offer(session, test_special_offer.id)

        # Assertions to validate the deletion of the special offer
        assert is_deleted

    # Clean-up
    await engine.dispose()
