from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model.models import Listing
from data.models import Listing as DBListing
from typing import List


def create_listing(db: Session, listing: Listing) -> DBListing:
    try:
        db_listing = DBListing(**listing.dict(exclude_unset=True))
        db.add(db_listing)
        db.commit()
        db.refresh(db_listing)
        return db_listing
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_all_listings(db: Session, skip: int = 0, limit: int = 10) -> List[DBListing]:
    return db.query(DBListing).offset(skip).limit(limit).all()
