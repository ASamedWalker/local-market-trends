import pytest
from uuid import uuid4
from sqlalchemy.future import select
from src.models.category import Category
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.services.category_service import (
    create_category,
    get_category,
    update_category,
    delete_category,
)


@pytest.mark.asyncio
async def test_create_category(async_session):
    async with async_session() as session:
        category_create = CategoryCreate(name="Test Category")
        category = await create_category(session, category_create)
        assert category.id is not None, "Category ID should not be None"
        assert category.name == "Test Category", "Category name should match the input"


@pytest.mark.asyncio
async def test_get_category(async_session):
    async with async_session() as session:
        # Create a category to ensure there's something to retrieve
        category_create = CategoryCreate(name="Test Get Category")
        created_category = await create_category(session, category_create)

        retrieved_category = await get_category(session, created_category.id)
        assert retrieved_category is not None, "Retrieved category should not be None"
        assert (
            retrieved_category.name == "Test Get Category"
        ), "Retrieved category name should match the created name"


@pytest.mark.asyncio
async def test_update_category(async_session):
    async with async_session() as session:
        # Create a category to update
        category_create = CategoryCreate(name="Before Update")
        category = await create_category(session, category_create)

        category_update = CategoryUpdate(name="After Update")
        updated_category = await update_category(session, category.id, category_update)
        assert updated_category is not None, "Updated category should not be None"
        assert (
            updated_category.name == "After Update"
        ), "Updated category name should match the update input"


@pytest.mark.asyncio
async def test_delete_category(async_session):
    async with async_session() as session:
        # Create a category to delete
        category_create = CategoryCreate(name="Test Delete")
        category = await create_category(session, category_create)

        await delete_category(session, category.id)

        deleted_category = await get_category(session, category.id)
        assert deleted_category is None, "Deleted category should not be retrievable"


@pytest.mark.asyncio
async def test_simple_db_query(async_session):
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        assert categories is not None  # This simply checks that the query can be run
