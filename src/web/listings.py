from fastapi import APIRouter, Depends, HTTPException
from model.models import Listing
from sqlalchemy.orm import Session
from data.database import get_db
from service.listing_service import create_listing, get_all_listings
from typing import List


router = APIRouter(prefix="/listings")


@router.post("/", response_model=Listing)
async def create_listing_endpoint(listing: Listing, db: Session = Depends(get_db)):
    try:
        return create_listing(db, listing)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Listing])
async def get_all_listings_endpoint(db: Session = Depends(get_db)):
    try:
        listings = get_all_listings(db)
        return listings
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
