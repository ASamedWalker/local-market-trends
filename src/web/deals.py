from fastapi import APIRouter
from typing import List
from model.Deal import Deal  # Adjust import path as needed

router = APIRouter()

# Dummy data for deals
fake_deals_db = [
    {
        "id": 1,
        "title": "Weekend Grocery Deals",
        "description": "Special discounts on groceries this weekend.",
        "valid_until": "2023-07-01",
        "discount_rate": 20,
        "url": "http://example.com/deals/groceries",
    }
]


@router.get("/deals/", response_model=List[Deal])
async def read_deals():
    return fake_deals_db
