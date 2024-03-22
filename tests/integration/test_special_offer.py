import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.data.database import get_session
from uuid import UUID, uuid4
from datetime import datetime
from httpx._transports.asgi import ASGITransport
from httpx import AsyncClient
from src.main import app
from datetime import timedelta


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


@pytest.mark.asyncio
async def test_create_special_offer(async_client):
    # Assuming you've corrected the service layer to use .model_dump()
    grocery_item_data = {
        "name": "Apple",
        "description": "A sweet apple",
        "category": "Fruit",  # Assuming your GroceryItem model expects a category
    }
    grocery_item_response = await async_client.post(
        "/grocery_item/", json=grocery_item_data
    )
    assert grocery_item_response.status_code == 200
    grocery_item = grocery_item_response.json()

    data = {
        "grocery_item_id": grocery_item[
            "id"
        ],  # No conversion needed if your API correctly handles UUIDs in JSON
        "description": "Buy one get one free!",
        "valid_from": datetime.now()
        .date()
        .isoformat(),  # Example of converting dates to ISO format strings
        "valid_to": (datetime.now().date() + timedelta(days=30)).isoformat(),
    }
    response = await async_client.post("/special_offer/", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_special_offer(async_client):
    # Assuming you've corrected the service layer to use .model_dump()
    grocery_item_data = {
        "name": "Apple",
        "description": "A sweet apple",
        "category": "Fruit",  # Assuming your GroceryItem model expects a category
    }
    grocery_item_response = await async_client.post(
        "/grocery_item/", json=grocery_item_data
    )
    assert grocery_item_response.status_code == 200
    grocery_item = grocery_item_response.json()

    data = {
        "grocery_item_id": grocery_item[
            "id"
        ],  # No conversion needed if your API correctly handles UUIDs in JSON
        "description": "Buy one get one free!",
        "valid_from": datetime.now()
        .date()
        .isoformat(),  # Example of converting dates to ISO format strings
        "valid_to": (datetime.now().date() + timedelta(days=30)).isoformat(),
    }
    response = await async_client.post("/special_offer/", json=data)
    assert response.status_code == 200

    special_offer = response.json()
    special_offer_id = special_offer["id"]

    response = await async_client.get(f"/special_offer/{special_offer_id}")
    assert response.status_code == 200
    assert response.json() == special_offer


@pytest.mark.asyncio
async def test_get_all_special_offers(async_client):
    # Assuming you've corrected the service layer to use .model_dump()
    grocery_item_data = {
        "name": "Apple",
        "description": "A sweet apple",
        "category": "Fruit",  # Assuming your GroceryItem model expects a category
    }
    grocery_item_response = await async_client.post(
        "/grocery_item/", json=grocery_item_data
    )
    assert grocery_item_response.status_code == 200
    grocery_item = grocery_item_response.json()

    data = {
        "grocery_item_id": grocery_item[
            "id"
        ],  # No conversion needed if your API correctly handles UUIDs in JSON
        "description": "Buy one get one free!",
        "valid_from": datetime.now()
        .date()
        .isoformat(),  # Example of converting dates to ISO format strings
        "valid_to": (datetime.now().date() + timedelta(days=30)).isoformat(),
    }
    response = await async_client.post("/special_offer/", json=data)
    assert response.status_code == 200

    response = await async_client.get("/special_offer/")
    assert response.status_code == 200
    assert response.json()[0] == response.json()[0]


@pytest.mark.asyncio
async def test_update_special_offer(async_client):
    # Assuming you've corrected the service layer to use .model_dump()
    grocery_item_data = {
        "name": "Apple",
        "description": "A sweet apple",
        "category": "Fruit",  # Assuming your GroceryItem model expects a category
    }
    grocery_item_response = await async_client.post(
        "/grocery_item/", json=grocery_item_data
    )
    assert grocery_item_response.status_code == 200
    grocery_item = grocery_item_response.json()

    data = {
        "grocery_item_id": grocery_item[
            "id"
        ],
        "description": "Buy one get one free!",
        "valid_from": datetime.now()
        .date()
        .isoformat(),  # Example of converting dates to ISO format strings
        "valid_to": (datetime.now().date() + timedelta(days=30)).isoformat(),
    }
    response = await async_client.post("/special_offer/", json=data)
    assert response.status_code == 200

    special_offer = response.json()
    special_offer_id = special_offer["id"]

    data = {
        "grocery_item_id": grocery_item[
            "id"
        ],
        "description": "Buy one get one free!",
        "valid_from": datetime.now()
        .date()
        .isoformat(),  # Example of converting dates to ISO format strings
        "valid_to": (datetime.now().date() + timedelta(days=30)).isoformat(),
    }
    response = await async_client.put(f"/special_offer/{special_offer_id}", json=data)
    assert response.status_code == 200
    assert response.json() == data
