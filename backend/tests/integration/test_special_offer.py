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
async def test_update_special_offer(async_client: AsyncClient):
    # Create a GroceryItem first to link with the SpecialOffer
    grocery_item_data = {
        "name": "Apple",
        "description": "A sweet apple",
        "category": "Fruit",
    }
    grocery_item_response = await async_client.post(
        "/grocery_item/", json=grocery_item_data
    )
    assert grocery_item_response.status_code == 200
    grocery_item = grocery_item_response.json()

    # Create a SpecialOffer linked to the GroceryItem
    special_offer_data = {
        "grocery_item_id": grocery_item["id"],
        "description": "20% off!",
        "valid_from": datetime.now().date().isoformat(),
        "valid_to": (datetime.now().date() + timedelta(days=15)).isoformat(),
    }
    special_offer_response = await async_client.post(
        "/special_offer/", json=special_offer_data
    )
    assert special_offer_response.status_code == 200
    special_offer = special_offer_response.json()

    # Update the SpecialOffer
    update_data = {
        "description": "Buy one get one free!",
        "valid_from": datetime.now().date().isoformat(),
        "valid_to": (datetime.now().date() + timedelta(days=30)).isoformat(),
    }
    update_response = await async_client.put(
        f"/special_offer/{special_offer['id']}", json=update_data
    )
    assert update_response.status_code == 200

    # Validate the updated fields
    updated_special_offer = update_response.json()
    assert updated_special_offer["description"] == update_data["description"]

    # Convert and compare datetime fields to ensure updates were applied correctly
    valid_from_updated = datetime.fromisoformat(
        updated_special_offer["valid_from"]
    ).date()
    valid_to_updated = datetime.fromisoformat(updated_special_offer["valid_to"]).date()
    assert valid_from_updated == datetime.now().date()
    assert valid_to_updated == (datetime.now().date() + timedelta(days=30))


@pytest.mark.asyncio
async def test_delete_special_offer(async_client: AsyncClient):
    # Create a GroceryItem first to link with the SpecialOffer
    grocery_item_data = {
        "name": "Apple",
        "description": "A sweet apple",
        "category": "Fruit",
    }
    grocery_item_response = await async_client.post(
        "/grocery_item/", json=grocery_item_data
    )
    assert grocery_item_response.status_code == 200
    grocery_item = grocery_item_response.json()

    # Create a SpecialOffer linked to the GroceryItem
    special_offer_data = {
        "grocery_item_id": grocery_item["id"],
        "description": "20% off!",
        "valid_from": datetime.now().date().isoformat(),
        "valid_to": (datetime.now().date() + timedelta(days=15)).isoformat(),
    }
    special_offer_response = await async_client.post(
        "/special_offer/", json=special_offer_data
    )
    assert special_offer_response.status_code == 200
    special_offer = special_offer_response.json()

    # Delete the SpecialOffer
    delete_response = await async_client.delete(f"/special_offer/{special_offer['id']}")
    assert delete_response.status_code == 204

    # Attempt to retrieve the deleted SpecialOffer
    get_response = await async_client.get(f"/special_offer/{special_offer['id']}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Special offer not found"}
