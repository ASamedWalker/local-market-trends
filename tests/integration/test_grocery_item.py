import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.data.database import get_session
from uuid import UUID, uuid4
from httpx._transports.asgi import ASGITransport
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="module")
async def async_client():
    """Setup for the entire module"""
    # Create an in-memory SQLite database for testing
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncTestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

    # Create tables asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Override the get_session dependency to use the in-memory database
    async def override_get_session():
        async with AsyncTestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


# Test creating a new grocery item
@pytest.mark.asyncio
async def test_create_grocery_item(async_client):
    """Test creating a new grocery item"""
    response = await async_client.post(
        "/grocery_item/",
        json={"name": "Apple", "description": "A sweet apple", "category": "Fruit"},
    )
    assert response.status_code == 200
    grocery_item = response.json()
    assert grocery_item["name"] == "Apple"
    assert grocery_item["description"] == "A sweet apple"
    assert grocery_item["category"] == "Fruit"
    assert "id" in grocery_item
    try:
        uuid_obj = UUID(grocery_item["id"])
        assert uuid_obj
    except ValueError:
        pytest.fail(f"The 'id' value {grocery_item['id']} is not a valid UUID.")


@pytest.mark.asyncio
async def test_get_grocery_item(async_client):
    """Test getting a grocery item"""
    # Create a new grocery item
    create_response = await async_client.post(
        "/grocery_item/",
        json={"name": "Apple", "description": "A sweet apple", "category": "Fruit"},
    )
    assert create_response.status_code == 200
    grocery_item = create_response.json()
    grocery_item_id = grocery_item["id"]

    # Retrieve the grocery item
    get_response = await async_client.get(f"/grocery_item/{grocery_item_id}")
    assert get_response.status_code == 200
    retrieved_grocery_item = get_response.json()
    assert retrieved_grocery_item == grocery_item


@pytest.mark.asyncio
async def test_get_all_grocery_items(async_client):
    """Test getting all grocery items"""
    # Create a new grocery item
    create_response = await async_client.post(
        "/grocery_item/",
        json={"name": "Apple", "description": "A sweet apple", "category": "Fruit"},
    )
    assert create_response.status_code == 200
    grocery_item = create_response.json()

    # Retrieve all grocery items
    get_response = await async_client.get("/grocery_item/")
    assert get_response.status_code == 200
    grocery_items = get_response.json()
    assert any(item["name"] == "Apple" for item in grocery_items)


@pytest.mark.asyncio
async def test_update_grocery_item(async_client):
    """Test updating a grocery item"""
    # Create a new grocery item
    create_response = await async_client.post(
        "/grocery_item/",
        json={"name": "Apple", "description": "A sweet apple", "category": "Fruit"},
    )
    assert create_response.status_code == 200
    grocery_item = create_response.json()
    grocery_item_id = grocery_item["id"]

    # Update the grocery item
    update_response = await async_client.put(
        f"/grocery_item/{grocery_item_id}",
        json={"name": "Banana", "description": "A ripe banana", "category": "Fruit"},
    )
    assert update_response.status_code == 200
    updated_grocery_item = update_response.json()
    assert updated_grocery_item["name"] == "Banana"
    assert updated_grocery_item["description"] == "A ripe banana"
    assert updated_grocery_item["category"] == "Fruit"
    assert updated_grocery_item["id"] == grocery_item_id


@pytest.mark.asyncio
async def test_delete_grocery_item(async_client):
    """Test deleting a grocery item"""
    # Create a new grocery item
    create_response = await async_client.post(
        "/grocery_item/",
        json={"name": "Apple", "description": "A sweet apple", "category": "Fruit"},
    )
    assert create_response.status_code == 200
    grocery_item = create_response.json()
    grocery_item_id = grocery_item["id"]

    # Delete the grocery item
    delete_response = await async_client.delete(f"/grocery_item/{grocery_item_id}")
    assert delete_response.status_code == 200
    deleted_grocery_item = delete_response.json()
    assert deleted_grocery_item == grocery_item

    # Ensure the grocery item was deleted
    get_response = await async_client.get(f"/grocery_item/{grocery_item_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Grocery item not found"}
