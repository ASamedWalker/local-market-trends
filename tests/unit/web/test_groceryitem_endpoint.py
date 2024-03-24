import pytest
from unittest.mock import AsyncMock
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from src.models.all_models import GroceryItem
from uuid import UUID, uuid4

from src.main import app


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
async def test_get_all_grocery_items(async_client, mock_session):
    """Test the get_all_grocery_items endpoint"""
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    response = await async_client.get("/grocery_items/")
    assert response.status_code == 200
    assert response.json() == []

