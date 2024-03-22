import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.data.database import get_session
from uuid import UUID, uuid4
from httpx import AsyncClient

from src.main import app
from src.models import (
    SpecialOffer,
    GroceryItem,
    Market,
    PriceRecord,
)


# Set up TestClient
client = TestClient(app)


def override_get_session(module):
    """Setup for the entire module"""
    # Create an in-memory SQLite database for testing
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, echo=True)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create the tables
    SQLModel.metadata.create_all(bind=engine)

    # Dependency override for the app's database session

    try:
        db = TestingSession()
        yield db
    finally:
        db.close()

    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_read_main():
    """Example test for a read operation"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_create_grocery_item():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/grocery_item/",
            json={"name": "apple", "description": "A fruit"},
        )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "apple"
    assert response_json["description"] == "A fruit"
    # Since 'id' is dynamically generated, assert its presence rather than its value
    assert "id" in response_json