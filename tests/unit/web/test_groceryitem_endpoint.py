import pytest
from unittest.mock import AsyncMock
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.database import get_session
from httpx import AsyncClient
from sqlmodel import SQLModel
from src.models.all_models import GroceryItem
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
async def test_get_all_grocery_items(async_client, mock_session):
    """Test the get_all_grocery_items endpoint"""
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    response = await async_client.get("/grocery_items/")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_grocery_item(async_client, mock_session):
    # Assuming `items_data` is the expected subset of the GroceryItem fields
    items_data = {
        "id": str(uuid4()),
        "name": "Milk",
        "description": "A gallon of milk",
        "category": "Dairy",
    }
    # Your existing setup code here...

    response = await async_client.post("/grocery_items/", json=items_data)
    assert response.status_code == 200
    response_data = response.json()

    # Adjusting assertion to compare relevant fields only
    for key in items_data:
        assert response_data[key] == items_data[key]


# Implementing a test for the grocery item endpoint using unnitest.mock.AsyncMock
@pytest.mark.asyncio
async def test_get_grocery_item(async_client, mock_session):
    # FAILED tests/unit/web/test_groceryitem_endpoint.py::test_get_grocery_item - assert 404 == 200
    grocery_item_id = str(uuid4())
    items_data = {
        "id": grocery_item_id,
        "name": "Milk",
        "description": "A gallon of milk",
        "category": "Dairy",
    }

    mock_session.execute.return_value.scalars.return_value.first.return_value = items_data

    response = await async_client.get(f"/grocery_items/{grocery_item_id}")
    assert response.status_code == 200
    assert response.json() == items_data
    response_data = response.json()
    assert response_data["id"] == grocery_item_id
    assert response_data["name"] == "Milk"
    assert response_data["description"] == "A gallon of milk"
    assert response_data["category"] == "Dairy"