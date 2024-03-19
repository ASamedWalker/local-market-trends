from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.data.database import get_session

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


def test_read_main():
    """Example test for a read operation"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# # Add more tests...
# def test_create_market():
#     """Example test for a create operation"""
#     response = client.post(
#         "/market/",
#         json={"name": "Test Market", "location": "Test Location"},
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Test Market"
#     assert data["location"] == "Test Location"


# def test_get_all_markets():
#     """Example test for a read operation"""
#     response = client.get("/market/")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 1
#     assert data[0]["name"] == "Test Market"
#     assert data[0]["location"] == "Test Location"
