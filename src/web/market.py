from fastapi import APIRouter, HTTPException
from model.market import Market
import fake.market as service
from typing import Optional, List

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/", response_model=List[Market])
def get_all_endpoint() -> List[Market]:
    return service.get_all()


@router.get("/{market_id}", response_model=Market)
def get_by_id_endpoint(market_id: str) -> Market:
    market = service.get_by_id(market_id)
    if market:
        return market
    raise HTTPException(status_code=404, detail="Market not found")


@router.post("/", response_model=Market)
def create_endpoint(market: Market) -> Market:
    return service.create(market)


@router.put("/{market_id}", response_model=Market)
def update_endpoint(market_id: str, market: Market) -> Market:
    updated_market = service.update(market_id, market)
    if updated_market:
        return updated_market
    raise HTTPException(status_code=404, detail="Market not found")


@router.delete("/{market_id}")
def delete_endpoint(market_id: str) -> None:
    deleted = service.delete(market_id)
    if deleted:
        return
    raise HTTPException(status_code=404, detail="Market not found")
