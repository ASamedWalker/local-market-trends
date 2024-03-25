import pytest
from unittest.mock import AsyncMock, patch, ANY
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.data.database import get_session
from httpx import AsyncClient
from sqlmodel import SQLModel
from src.models.all_models import PriceRecord
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
async def test_create_price_record(async_client, mocker):
    price_record_data = {
        "id": str(uuid4()),
        "grocery_item_id": str(uuid4()),
        "market_id": str(uuid4()),
        "price": 1.99,
        "is_promotional": False,
        "promotional_details": None,
        "date_recorded": datetime.now().isoformat(),
    }

    # Create a PriceRecord object from price_record_data
    price_record = PriceRecord(**price_record_data)

    mock_create_price_record = mocker.patch(
        "src.web.price_record.create_price_record", return_value=price_record
    )

    response = await async_client.post("/price_records/", json=price_record_data)
    assert response.status_code == 200
    assert response.json() == price_record_data
    mock_create_price_record.assert_called_once()
    args, _ = mock_create_price_record.call_args
    assert args[0] == ANY
    # Ignore _sa_instance_state key when comparing PriceRecord object to expected dictionary
    assert {
        k: v for k, v in args[1].__dict__.items() if k != "_sa_instance_state"
    } == price_record_data


@pytest.mark.asyncio
async def test_get_price_record(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    price_record_data = {
        "id": str(fixed_uuid),
        "grocery_item_id": str(uuid4()),
        "market_id": str(uuid4()),
        "price": 1.99,
        "is_promotional": False,
        "promotional_details": None,
        "date_recorded": datetime.now().isoformat(),
    }

    mock_get_price_record = mocker.patch(
        "src.web.price_record.get_price_record", return_value=price_record_data
    )

    response = await async_client.get(f"/price_records/{fixed_uuid}")
    assert response.status_code == 200
    assert response.json() == price_record_data
    mock_get_price_record.assert_called_once()
    args, _ = mock_get_price_record.call_args
    assert args[0] == ANY
    assert args[1] == fixed_uuid


@pytest.mark.asyncio
async def test_get_all_price_records(async_client, mocker):
    price_record_data = [
        {
            "id": str(uuid4()),
            "grocery_item_id": str(uuid4()),
            "market_id": str(uuid4()),
            "price": 1.99,
            "is_promotional": False,
            "promotional_details": None,
            "date_recorded": datetime.now().isoformat(),
        }
    ]

    mock_get_all_price_records = mocker.patch(
        "src.web.price_record.get_all_price_records", return_value=price_record_data
    )

    response = await async_client.get("/price_records/")
    assert response.status_code == 200
    assert response.json() == price_record_data
    mock_get_all_price_records.assert_called_once()
    args, _ = mock_get_all_price_records.call_args
    assert args[0] == ANY


@pytest.mark.asyncio
async def test_update_price_record(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    original_price_record_data = {
        "id": str(fixed_uuid),
        "grocery_item_id": str(uuid4()),
        "market_id": str(uuid4()),
        "price": 1.99,
        "is_promotional": False,
        "promotional_details": None,
        "date_recorded": datetime.now().isoformat(),
    }
    updated_price_record_data = {
        "id": str(fixed_uuid),
        "grocery_item_id": str(uuid4()),
        "market_id": str(uuid4()),
        "price": 2.99,
        "is_promotional": True,
        "promotional_details": "Buy one get one free",
        "date_recorded": datetime.now().isoformat(),
    }

    mock_update_price_record = mocker.patch(
        "src.web.price_record.update_price_record",
        return_value=updated_price_record_data,
    )

    response = await async_client.put(
        f"/price_records/{str(fixed_uuid)}", json=updated_price_record_data
    )
    assert response.status_code == 200
    assert response.json() == updated_price_record_data
    mock_update_price_record.assert_called_once()
    args, _ = mock_update_price_record.call_args
    assert args[0] == ANY
    assert args[1] == fixed_uuid
    # Ignore _sa_instance_state key when comparing PriceRecord object to expected dictionary
    assert {
        k: v for k, v in args[2].__dict__.items() if k != "_sa_instance_state"
    } == updated_price_record_data


@pytest.mark.asyncio
async def test_delete_price_record(async_client, mocker):
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")
    price_record_data = {
        "id": str(fixed_uuid),
        "grocery_item_id": str(uuid4()),
        "market_id": str(uuid4()),
        "price": 1.99,
        "is_promotional": False,
        "promotional_details": None,
        "date_recorded": datetime.now().isoformat(),
    }

    mock_delete_price_record = mocker.patch(
        "src.web.price_record.delete_price_record", return_value=price_record_data
    )

    response = await async_client.delete(f"/price_records/{fixed_uuid}")
    assert response.status_code == 200
    assert response.json() == price_record_data
    mock_delete_price_record.assert_called_once()
    args, _ = mock_delete_price_record.call_args
    assert args[0] == ANY
    assert args[1] == fixed_uuid
