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


# Test creating a new market
@pytest.mark.asyncio
async def test_create_market(async_client):
    """Test creating a new market"""
    # market has a name, location_description, latitude, and longitude
    data = {
        "name": "Test Market",
        "location_description": "Test Location",
        "latitude": 1.0,
        "longitude": 1.0,
    }
    response = await async_client.post("/market/", json=data)
    assert response.status_code == 200
    market = response.json()
    assert market["name"] == "Test Market"
    assert market["location_description"] == "Test Location"
    assert market["latitude"] == 1.0
    assert market["longitude"] == 1.0
    assert "id" in market
    try:
        uuid_obj = UUID(market["id"])
        assert uuid_obj
    except ValueError:
        pytest.fail(f"The 'id' value {market['id']} is not a valid UUID.")


@pytest.mark.asyncio
async def test_get_market(async_client):
    """Test getting a market"""
    # Create a new market
    create_response = await async_client.post(
        "/market/",
        json={
            "name": "Test Market",
            "location_description": "Test Location",
            "latitude": 1.0,
            "longitude": 1.0,
        },
    )
    market = create_response.json()
    market_id = market["id"]

    # Get the market
    get_response = await async_client.get(f"/market/{market_id}")
    assert get_response.status_code == 200
    market = get_response.json()
    assert market["name"] == "Test Market"
    assert market["location_description"] == "Test Location"
    assert market["latitude"] == 1.0
    assert market["longitude"] == 1.0
    assert market["id"] == market_id


@pytest.mark.asyncio
async def test_get_all_markets(async_client):
    """Test getting all markets"""
    # Create a new market
    create_response = await async_client.post(
        "/market/",
        json={
            "name": "Test Market",
            "location_description": "Test Location",
            "latitude": 1.0,
            "longitude": 1.0,
        },
    )
    assert create_response.status_code == 200

    # Get all markets
    get_response = await async_client.get("/market/")
    assert get_response.status_code == 200
    markets = get_response.json()
    market = markets[0]
    assert market["name"] == "Test Market"
    assert market["location_description"] == "Test Location"
    assert market["latitude"] == 1.0
    assert market["longitude"] == 1.0
    assert "id" in market
    try:
        uuid_obj = UUID(market["id"])
        assert uuid_obj
    except ValueError:
        pytest.fail(f"The 'id' value {market['id']} is not a valid UUID.")


@pytest.mark.asyncio
async def test_update_market(async_client):
    """Test updating a market"""
    # Create a new market
    create_response = await async_client.post(
        "/market/",
        json={
            "name": "Test Market",
            "location_description": "Test Location",
            "latitude": 1.0,
            "longitude": 1.0,
        },
    )
    assert create_response.status_code == 200
    market = create_response.json()
    market_id = market["id"]

    # Update the market
    update_response = await async_client.put(
        f"/market/{market_id}",
        json={
            "name": "Updated Market",
            "location_description": "Updated Location",
            "latitude": 2.0,
            "longitude": 2.0,
        },
    )
    assert update_response.status_code == 200
    updated_market = update_response.json()
    assert updated_market["name"] == "Updated Market"
    assert updated_market["location_description"] == "Updated Location"
    assert updated_market["latitude"] == 2.0
    assert updated_market["longitude"] == 2.0
    assert updated_market["id"] == market_id


@pytest.mark.asyncio
async def test_delete_market(async_client):
    """Test deleting a market"""
    # Create a new market
    create_response = await async_client.post(
        "/market/",
        json={
            "name": "Test Market",
            "location_description": "Test Location",
            "latitude": 1.0,
            "longitude": 1.0,
        },
    )
    assert create_response.status_code == 200
    market = create_response.json()
    market_id = market["id"]

    # Delete the market
    delete_response = await async_client.delete(f"/market/{market_id}")
    assert delete_response.status_code == 200
    # deleted_market = delete_response.json()
    # assert deleted_market["name"] == "Test Market"
    # assert deleted_market["location_description"] == "Test Location"
    # assert deleted_market["latitude"] == 1.0
    # assert deleted_market["longitude"] == 1.0
    # assert deleted_market["id"] == market_id

    # Ensure the market was deleted
    get_response = await async_client.get(f"/market/{market_id}")
    assert get_response.status_code == 404
    # assert get_response.json() == {"detail": "Market not found"}
