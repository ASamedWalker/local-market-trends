from src.model.models import Listing, MarketTrend, MarketType
from faker import Faker
import random


fake = Faker()


# Generate fake listings
def generate_fake_listings(n=10):
    return [
        Listing(
            id=str(fake.uuid4()),
            title=fake.sentence(nb_words=6),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(10.0, 1000.0), 2),
            market_type=random.choice(list(MarketType)).value,
        )
        for _ in range(n)
    ]


# Generate fake Market trends
def generate_fake_market_trends(n=5):
    return [
        MarketTrend(
            market_type=random.choice(list(MarketType)).value,
            trend_description=fake.paragraph(nb_sentences=3),
        )
        for _ in range(n)
    ]
