# Lets create a review service to interact with the Review model
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID

from models.all_models import Review

async def create_review(
    session: AsyncSession, review: Review
) -> Review:
    try:
        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_review(
    session: AsyncSession, review_id: UUID
) -> Optional[Review]:
    try:
        result = await session.get(Review, review_id)
        if not result:
            raise HTTPException(status_code=404, detail="Review not found")
        return result
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_reviews(session: AsyncSession) -> List[Review]:
    try:
        result = await session.execute(select(Review))
        reviews = result.scalars().all()
        return reviews
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_reviews_by_grocery_item_id(
    session: AsyncSession, grocery_item_id: UUID
) -> List[Review]:
    try:
        result = await session.execute(select(Review).where(Review.grocery_item_id == grocery_item_id))
        reviews = result.scalars().all()
        return reviews
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_review(
    session: AsyncSession, review_id: UUID, review_data: dict
) -> Optional[Review]:
    try:
        review = await session.get(Review, review_id)
        if review:
            review_data.id = review_id  # Ensure ID remains unchanged
            await session.merge(review_data)
            await session.commit()
            return review_data
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def delete_review(
    session: AsyncSession, review_id: UUID
) -> Optional[Review]:
    try:
        review = await session.get(Review, review_id)
        if review:
            await session.delete(review)
            await session.commit()
            return review
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# You may want to create a function to calculate the average rating for a grocery item
async def calculate_average_rating(session: AsyncSession, grocery_item_id: UUID) -> float:
    result = await session.execute(
        select(
            func.avg(Review.rating).label("average")
        ).where(
            Review.grocery_item_id == grocery_item_id
        )
    )
    average_rating = result.scalar_one_or_none()
    return average_rating if average_rating else 0.0


# Nows lets build the API endpoints for the Review model
