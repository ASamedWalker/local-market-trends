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


@pytest.mark.asyncio
async def test_create_price_record(async_client):
    """Test creating a new price record"""
    # price record has a grocery_item_id, market_id, price, date_recorded,
    # is_promotional, promotional_details
    data = {
        "grocery_item_id": str(uuid4()),
        "market_id": str(uuid4()),
        "price": 1.0,
        "is_promotional": False,
    }
    response = await async_client.post("/price_record/", json=data)
    assert response.status_code == 200
    price_record = response.json()
    assert price_record["grocery_item_id"] == data["grocery_item_id"]
    assert price_record["market_id"] == data["market_id"]
    assert price_record["price"] == 1.0
    assert price_record["is_promotional"] == False
    assert "id" in price_record
    assert "date_recorded" in price_record
    assert "promotional_details" in price_record
    try:
        uuid_obj = UUID(price_record["id"])
        assert uuid_obj
    except ValueError:
        assert False  # Fail the test if the UUID is invalid


@pytest.mark.asyncio
async def test_get_all_price_records(async_client):
    """Test getting all price records"""
    # Create a new price record
    create_response = await async_client.post(
        "/price_record/",
        json={
            "grocery_item_id": str(uuid4()),
            "market_id": str(uuid4()),
            "price": 1.0,
            "is_promotional": False,
        },
    )
    assert create_response.status_code == 200

    # Get all price records
    response = await async_client.get("/price_record/")
    assert response.status_code == 200
    price_records = response.json()
    price_record = price_records[0]
    assert "id" in price_record
    assert "date_recorded" in price_record
    assert "promotional_details" in price_record


@pytest.mark.asyncio
async def test_get_price_record(async_client):
    """Test getting a price record"""
    # Create a new price record
    create_response = await async_client.post(
        "/price_record/",
        json={
            "grocery_item_id": str(uuid4()),
            "market_id": str(uuid4()),
            "price": 1.0,
            "is_promotional": False,
        },
    )
    price_record = create_response.json()
    price_record_id = price_record["id"]

    # Get the price record
    get_response = await async_client.get(f"/price_record/{price_record_id}")
    assert get_response.status_code == 200
    price_record = get_response.json()
    assert price_record["price"] == 1.0
    assert price_record["is_promotional"] == False
    assert price_record["id"] == price_record_id


@pytest.mark.asyncio
async def test_update_price_record(async_client):
    """Test updating a price record"""
    # Create a new price record
    create_response = await async_client.post(
        "/price_record/",
        json={
            "grocery_item_id": str(uuid4()),
            "market_id": str(uuid4()),
            "price": 1.0,
            "is_promotional": False,
        },
    )
    price_record = create_response.json()
    price_record_id = price_record["id"]

    # Update the price record
    update_response = await async_client.put(
        f"/price_record/{price_record_id}",
        json={
            "grocery_item_id": str(uuid4()),
            "market_id": str(uuid4()),
            "price": 2.0,
            "is_promotional": True,
        },
    )
    assert update_response.status_code == 200
    updated_price_record = update_response.json()
    assert updated_price_record["price"] == 2.0
    assert updated_price_record["is_promotional"] == True
    assert updated_price_record["id"] == price_record_id


@pytest.mark.asyncio
async def test_delete_price_record(async_client):
    """Test deleting a price record"""
    # Create a new price record
    create_response = await async_client.post(
        "/price_record/",
        json={
            "grocery_item_id": str(uuid4()),
            "market_id": str(uuid4()),
            "price": 1.0,
            "is_promotional": False,
        },
    )
    price_record = create_response.json()
    price_record_id = price_record["id"]

    # Delete the price record
    delete_response = await async_client.delete(f"/price_record/{price_record_id}")
    assert delete_response.status_code == 200
    # deleted_price_record = delete_response.json()
    # assert deleted_price_record["price"] == 1.0
    # assert deleted_price_record["is_promotional"] == False
    # assert deleted_price_record["id"] == price_record_id
