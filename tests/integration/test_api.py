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


@app.on_event("startup")
def override_dependencies():
    """Override get_session dependency with one that uses the test database."""
    app.dependency_overrides[get_session] = override_get_session


def test_read_main():
    """Example test for a read operation"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
