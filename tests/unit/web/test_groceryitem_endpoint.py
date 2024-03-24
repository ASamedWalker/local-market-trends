import pytest
from unittest.mock import AsyncMock
from src.main import app
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from src.models.grocery_item import GroceryItem


# Implementing a test for the grocery item endpoint using unnitest.mock.AsyncMock
@pytest.fixture(scope="module")
async def async_client():
    """Setup for the entire module"""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def mock_session(mocker):
    mock = mocker.patch("src.data.database.get_session", autospec=True)
    session_mock = AsyncMock(spec=AsyncSession)
    mock.return_value = session_mock
    yield session_mock


@pytest.mark.asyncio
async def test_create_grocery_item(async_client, mock_session):
    item_data = {"name": "Milk", "description": "A gallon of milk", "category": "Dairy"}
    mock_session.execute.return_value.scalars.return_value.first.return_value = (
        GroceryItem(**item_data)
    )

    response = await async_client.post("/grocery-items/", json=item_data)
    assert response.status_code == 200
    assert (
        response.json() == item_data
    )  # Simplified, adjust based on actual response structure

    # Verify session interactions, like commit calls if applicable
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_grocery_items(async_client, mock_session):
    items_data = [
        {
            "id": 1,
            "name": "Milk",
            "description": "A gallon of milk",
            "category": "Dairy",
        },
        {
            "id": 2,
            "name": "Bread",
            "description": "A loaf of bread",
            "category": "Bakery",
        },
    ]
    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        GroceryItem(**item) for item in items_data
    ]

    response = await async_client.get("/grocery-items/")
    assert response.status_code == 200
    assert response.json() == items_data

    # Verify session interactions
    # mock_session.query.assert_called_with(GroceryItem)
