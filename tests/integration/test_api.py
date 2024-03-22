import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.data.database import get_session
from uuid import UUID, uuid4
from httpx import AsyncClient

from src.main import app


# client = httpx.AsyncClient(app=app, base_url="http://test")


@pytest.fixture(scope="module")
async def async_client():
    """Setup for the entire module"""
    # Create an in-memory SQLite database for testing
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, echo=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    SQLModel.metadata.create_all(bind=engine)

    # Dependency override for the app's database session

    # Override the get_session dependency to use the in-memory database
    def override_get_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_read_main(async_client):
    """Example test for a read operation"""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_create_grocery_item(async_client):
    """Example test for a create operation"""
    response = await async_client.post(
        "/grocery_item/",
        json={
            "name": "apple",
            "description": "A fruit",
            "category": "Fruits",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "apple"
    assert response_json["description"] == "A fruit"
    assert "id" in response_json
