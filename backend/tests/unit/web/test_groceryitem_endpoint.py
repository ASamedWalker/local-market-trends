import pytest
from unittest.mock import AsyncMock, patch, ANY
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.database import get_session
from httpx import AsyncClient
from sqlmodel import SQLModel
from src.models.all_models import GroceryItem
from src.services.grocery_item_service import update_grocery_item
from uuid import UUID, uuid4

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
async def test_create_grocery_item(async_client, mock_session):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    grocery_item_data = {
        "id": str(fixed_uuid),
        "name": "Milk",
        "description": "A gallon of milk",
        "category": "Dairy",
        "image_url": None,
    }

    mock_session.execute.return_value.scalar.return_value.first.return_value = (
        grocery_item_data
    )
    with patch("uuid.uuid4", return_value=fixed_uuid):

        response = await async_client.post("/grocery_items/", json=grocery_item_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == grocery_item_data["name"]
        assert response_data["description"] == grocery_item_data["description"]
        assert response_data["category"] == grocery_item_data["category"]
        assert response_data["id"] == str(fixed_uuid)
        assert response_data["image_url"] is None


@pytest.mark.asyncio
async def test_get_grocery_item(async_client, mock_session):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_item_data = {
        "id": str(fixed_uuid),
        "name": "Milk",
        "description": "A gallon of milk",
        "category": "Dairy",
        "image_url": None,
    }

    mock_session.get.return_value = mock_item_data

    with patch("uuid.uuid4", return_value=fixed_uuid):
        mock_item_id = str(fixed_uuid)
        response = await async_client.get(f"/grocery_items/{mock_item_id}")
        assert response.status_code == 200
        assert response.json() == mock_item_data


@pytest.mark.asyncio
async def test_get_all_grocery_items(async_client, mock_session):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    mock_item_data = {
        "id": str(fixed_uuid),
        "name": "Milk",
        "description": "A gallon of milk",
        "category": "Dairy",
        "image_url": None,
    }

    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        mock_item_data
    ]

    response = await async_client.get("/grocery_items/")
    assert response.status_code == 200
    assert response.json() == [mock_item_data]


@pytest.mark.asyncio
async def test_update_grocery_item(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    original_item_data = {
        "id": str(fixed_uuid),
        "name": "Milk",
        "description": "A gallon of milk",
        "category": "Dairy",
        "image_url": None,
    }
    updated_item_data = {
        "id": str(fixed_uuid),
        "name": "Almond Milk",
        "description": "A gallon of almond milk",
        "category": "Dairy",
        "image_url": None,
    }

    mock_update_grocery_item = mocker.patch(
        "src.web.grocery_item.update_grocery_item", return_value=updated_item_data
    )

    response = await async_client.put(
        f"/grocery_items/{str(fixed_uuid)}", json=updated_item_data
    )
    assert response.status_code == 200
    assert response.json() == updated_item_data
    mock_update_grocery_item.assert_called_once_with(ANY, fixed_uuid, updated_item_data)


@pytest.mark.asyncio
async def test_update_grocery_item_not_found(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    updated_item_data = {
        "id": str(fixed_uuid),
        "name": "Almond Milk",
        "description": "A gallon of almond milk",
        "category": "Dairy",
        "image_url": None,
    }

    mock_update_grocery_item = mocker.patch(
        "src.web.grocery_item.update_grocery_item", return_value=None
    )

    response = await async_client.put(
        f"/grocery_items/{str(fixed_uuid)}", json=updated_item_data
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Grocery item not found"}
    mock_update_grocery_item.assert_called_once_with(ANY, fixed_uuid, updated_item_data)
