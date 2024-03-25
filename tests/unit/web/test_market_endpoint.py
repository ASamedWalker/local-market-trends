import pytest
from unittest.mock import AsyncMock, patch, ANY
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.database import get_session
from httpx import AsyncClient
from sqlmodel import SQLModel
from src.models.all_models import Market
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
async def test_create_market(async_client, mocker):
    market_data = {
        "id": str(uuid4()),
        "name": "Test Market",
        "location_description": "Test Location",
        "latitude": 12.34,
        "longitude": 56.78,
    }

    # Create a Market object from market_data
    market = Market(**market_data)

    mock_create_market = mocker.patch(
        "src.web.market.create_market", return_value=market
    )

    response = await async_client.post("/markets/", json=market_data)
    assert response.status_code == 200
    assert response.json() == market_data
    mock_create_market.assert_called_once()
    args, _ = mock_create_market.call_args
    assert args[0] == ANY
    # Ignore _sa_instance_state key when comparing Market object to expected dictionary
    assert {
        k: v for k, v in args[1].__dict__.items() if k != "_sa_instance_state"
    } == market_data


@pytest.mark.asyncio
async def test_get_market(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    market_data = {
        "id": str(fixed_uuid),
        "name": "Test Market",
        "location_description": "Test Location",
        "latitude": 12.34,
        "longitude": 56.78,
    }

    mock_get_market = mocker.patch(
        "src.web.market.get_market", return_value=market_data
    )

    response = await async_client.get(f"/markets/{str(fixed_uuid)}")
    assert response.status_code == 200
    assert response.json() == market_data
    mock_get_market.assert_called_once_with(ANY, fixed_uuid)


@pytest.mark.asyncio
async def test_get_all_markets(async_client, mocker):
    market_data = [
        {
            "id": str(uuid4()),
            "name": "Test Market 1",
            "location_description": "Test Location 1",
            "latitude": 12.34,
            "longitude": 56.78,
        },
        {
            "id": str(uuid4()),
            "name": "Test Market 2",
            "location_description": "Test Location 2",
            "latitude": 23.45,
            "longitude": 67.89,
        },
    ]

    mock_get_all_markets = mocker.patch(
        "src.web.market.get_all_markets", return_value=market_data
    )

    response = await async_client.get("/markets/")
    assert response.status_code == 200
    assert response.json() == market_data
    mock_get_all_markets.assert_called_once_with(ANY)


@pytest.mark.asyncio
async def test_update_market(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    original_market_data = {
        "id": str(fixed_uuid),
        "name": "Test Market",
        "location_description": "Test Location",
        "latitude": 12.34,
        "longitude": 56.78,
    }
    updated_market_data = {
        "id": str(fixed_uuid),
        "name": "Updated Test Market",
        "location_description": "Updated Test Location",
        "latitude": 23.45,
        "longitude": 67.89,
    }

    # Create a Market object from updated_market_data
    updated_market = Market(**updated_market_data)

    mock_update_market = mocker.patch(
        "src.web.market.update_market", return_value=updated_market
    )

    response = await async_client.put(
        f"/markets/{str(fixed_uuid)}", json=updated_market_data
    )
    assert response.status_code == 200
    assert response.json() == updated_market_data
    mock_update_market.assert_called_once()
    args, _ = mock_update_market.call_args
    assert args[0] == ANY
    assert args[1] == fixed_uuid
    # Ignore _sa_instance_state key when comparing Market object to expected dictionary
    assert {
        k: v for k, v in args[2].__dict__.items() if k != "_sa_instance_state"
    } == updated_market_data


@pytest.mark.asyncio
async def test_delete_market(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    market_data = {
        "id": str(fixed_uuid),
        "name": "Test Market",
        "location_description": "Test Location",
        "latitude": 12.34,
        "longitude": 56.78,
    }

    mock_delete_market = mocker.patch(
        "src.web.market.delete_market", return_value=market_data
    )

    response = await async_client.delete(f"/markets/{str(fixed_uuid)}")
    assert response.status_code == 200
    assert response.json() == market_data
    mock_delete_market.assert_called_once_with(ANY, fixed_uuid)
