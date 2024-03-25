import pytest
import json
from unittest.mock import AsyncMock, patch, ANY
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.database import get_session
from httpx import AsyncClient
from sqlmodel import SQLModel
from src.models.all_models import SpecialOffer
from src.schemas.special_offer import SpecialOfferCreate
from src.services.special_offer_service import create_special_offer_service
from uuid import UUID, uuid4
from datetime import datetime

from src.main import app


# Implementing a test for the grocery item endpoint using unnitest.mock.AsyncMock
@pytest.fixture(scope="module")
async def async_client():
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncTestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async def override_get_session():
        async with AsyncTestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def mock_session(mocker):
    mock = mocker.patch("src.data.database.get_session", autospec=True)
    session_mock = AsyncMock(spec=AsyncSession)
    mock.return_value = session_mock
    yield session_mock


@pytest.mark.asyncio
async def test_create_special_offer(async_client):
    special_offer_data = {
        "grocery_item_id": str(uuid4()),
        "description": "Buy one get one free",
        "valid_from": datetime.now().isoformat(),
        "valid_to": datetime.now().isoformat(),
        "image_url": None,
    }

    response = await async_client.post("/special_offers/", json=special_offer_data)
    assert response.status_code == 200

    # Check that the id field in the response is a valid UUID
    try:
        UUID(response.json()["id"], version=4)
    except ValueError:
        assert False, "id field in response is not a valid UUID"

    # Check that the response contains the correct special offer data
    for key in special_offer_data:
        assert response.json()[key] == special_offer_data[key]


@pytest.mark.asyncio
async def test_get_special_offer(async_client):
    # Create a special offer
    special_offer_data = {
        "grocery_item_id": str(uuid4()),
        "description": "Buy one get one free",
        "valid_from": datetime.now().isoformat(),
        "valid_to": datetime.now().isoformat(),
        "image_url": None,
    }
    create_response = await async_client.post(
        "/special_offers/", json=special_offer_data
    )
    assert create_response.status_code == 200

    # Get the id of the created special offer
    special_offer_id = create_response.json()["id"]

    # Get the special offer
    get_response = await async_client.get(f"/special_offers/{special_offer_id}")
    assert get_response.status_code == 200

    try:
        UUID(get_response.json()["id"], version=4)
    except ValueError:
        assert False, "id field in response is not a valid UUID"

    # Check that the response contains the correct special offer data
    for key in special_offer_data:
        assert get_response.json()[key] == special_offer_data[key]


@pytest.mark.asyncio
async def test_get_all_special_offers(async_client):
    # Assuming you have an endpoint to get all special offers
    response = await async_client.get("/special_offers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_special_offer(async_client):
    # Create a special offer
    special_offer_data = {
        "grocery_item_id": str(uuid4()),
        "description": "Buy one get one free",
        "valid_from": datetime.now().isoformat(),
        "valid_to": datetime.now().isoformat(),
        "image_url": None,
    }
    create_response = await async_client.post(
        "/special_offers/", json=special_offer_data
    )
    assert create_response.status_code == 200

    # Get the id of the created special offer
    special_offer_id = create_response.json()["id"]

    # Update the special offer
    update_data = {"description": "Buy two get one free"}
    update_response = await async_client.put(
        f"/special_offers/{special_offer_id}", json=update_data
    )
    assert update_response.status_code == 200

    # Check that the response contains the updated data
    assert update_response.json()["description"] == update_data["description"]


@pytest.mark.asyncio
async def test_delete_special_offer(async_client):
    # Create a special offer
    special_offer_data = {
        "grocery_item_id": str(uuid4()),
        "description": "Buy one get one free",
        "valid_from": datetime.now().isoformat(),
        "valid_to": datetime.now().isoformat(),
        "image_url": None,
    }
    create_response = await async_client.post(
        "/special_offers/", json=special_offer_data
    )
    assert create_response.status_code == 200

    # Get the id of the created special offer
    special_offer_id = create_response.json()["id"]

    # Delete the special offer
    delete_response = await async_client.delete(f"/special_offers/{special_offer_id}")
    assert delete_response.status_code == 204  # Expect a 204 status code
