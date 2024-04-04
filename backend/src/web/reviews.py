# Nows lets build the API endpoints for the Review model
from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import Optional, List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from data.database import get_session
from services.review_service import (
    create_review,
    get_review,
    get_all_reviews,
    get_reviews_by_grocery_item_id,
    update_review,
    delete_review,
)

from models.all_models import Review

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=Review)
async def create_review_endpoint(
    review: Review, session: AsyncSession = Depends(get_session)
) -> Review:
    return await create_review(session, review)

@router.get("/{review_id}", response_model=Review)
async def get_review_endpoint(
    review_id: UUID, session: AsyncSession = Depends(get_session)
) -> Review:
    review = await get_review(session, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return review

@router.get("/", response_model=List[Review])
async def get_all_reviews_endpoint(
    session: AsyncSession = Depends(get_session),
) -> List[Review]:
    return await get_all_reviews(session)


@router.get("/item/{grocery_item_id}", response_model=List[Review])
async def get_reviews_by_grocery_item_id_endpoint(
    grocery_item_id: UUID, session: AsyncSession = Depends(get_session)
) -> List[Review]:
    return await get_reviews_by_grocery_item_id(session, grocery_item_id)

@router.put("/{review_id}", response_model=Review)
async def update_review_endpoint(
    review_id: UUID,
    review: dict,
    session: AsyncSession = Depends(get_session),
) -> Review:
    updated_review = await update_review(session, review_id, review)
    if not updated_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return updated_review

@router.delete("/{review_id}", response_model=Review)
async def delete_review_endpoint(
    review_id: UUID, session: AsyncSession = Depends(get_session)
) -> Review:
    review = await delete_review(session, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return review