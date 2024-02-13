from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_listing():
    response = client.post(
        "/listings/",
        json={
            "title": "Sample Listing",
            "description": "A detailed description",
            "price": 100.0,
            "market_type": "real estate",
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Listing"


def test_get_listings():
    response = client.get("/listings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
