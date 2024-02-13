def test_create_listing(test_db_session):
    from service.listing_service import create_listing

    # Assume ListingCreate is a Pydantic model for creating listings
    from model.models import ListingCreate

    new_listing = ListingCreate(
        title="Test",
        description="Test Description",
        price=100.0,
        market_type="real estate",
    )
    result = create_listing(db=test_db_session, listing=new_listing)
    assert result.title == new_listing.title
