from model.market import Market
from typing import Optional, List
from uuid import UUID, uuid4


# Simulated market data
_markets = [
    Market(
        id=uuid4(),
        name="Downtown Farmers' Market",
        location_description="Central Plaza, Downtown",
        latitude=37.7749,
        longitude=-122.4194,
    ),
    Market(
        id=uuid4(),
        name="Uptown Grocery Market",
        location_description="Uptown District, Near the River",
        latitude=37.8044,
        longitude=-122.2711,
    ),
    Market(
        id=uuid4(),
        name="Westside Organic Market",
        location_description="Westside Shopping Center",
        latitude=37.7749,
        longitude=-122.4194,
    ),
]


def get_all() -> list[Market]:
    return _markets


def get_by_id(market_id: UUID) -> Market:
    for market in _markets:
        if market.id == id:
            return market
    return None


def create(market: Market) -> Market:
    _markets.append(market)
    return market


def update(market_id: UUID, updated_market: Market) -> Market:
    for i, market in enumerate(_markets):
        if market.id == market.id:
            _markets[i] = updated_market
            return updated_market
    return None


def delete(market_id: UUID) -> Market:
    for i, market in enumerate(_markets):
        if market.id == market.id:
            del _markets[i]
            return True
    return False
