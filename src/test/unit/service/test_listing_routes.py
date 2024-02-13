def test_read_listings(test_client):
    response = test_client.get("/listings/")
    assert response.status_code == 200
    # Further assertions based on response content
