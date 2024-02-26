from model import Listing
from service import listing as code
from uuid import UUID, uuid4

sample = Listing(
    id=uuid4(),
    title="Lenovo ThinkPad X1 Carbon",  # change this to "Lenovo ThinkPad X1 Carbon"
    description="2021 Model, 16GB RAM, 512GB SSD, M1 Pro chip.",
    price=3000.0,
    category_id=uuid4(),
    location_id=uuid4(),
)


def test_create():
    assert code.create(sample) == sample
    assert code.get_one("Lenovo ThinkPad X1 Carbon") == sample


def test_get_exists():
    assert code.get_one("Lenovo ThinkPad X1 Carbon") == sample


def test_get_missing():
    assert code.get_one("Nonexistent Listing") is None
