import pytest
from model.models import MarketTrend, MarketType
from service.market_trend_service import create_market_trend, get_all_market_trends


@pytest.fixture
def market_trend_data():
    return MarketTrend(
        market_type=MarketType.real_estate,
        trend_description="Growing interest in suburban areas",
    )


def test_create_market_trend(market_trend_data):
    result = create_market_trend(market_trend_data)
    assert result == market_trend_data


def test_get_all_market_trends(market_trend_data):
    create_market_trend(market_trend_data)
    result = get_all_market_trends()
    assert market_trend_data in result
