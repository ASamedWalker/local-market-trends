from fastapi import Depends, APIRouter
from sqlmodel import Session

from src.data.database import (
    get_session,
)  # Make sure this import path matches your project structure

router = APIRouter()


@router.get("/")
def read_root(db: Session = Depends(get_session)):
    # Use 'db' to interact with the database within the route
    return {"message": "Hello World"}
