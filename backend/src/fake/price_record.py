from model.price_record import PriceRecord
from uuid import UUID, uuid4
from datetime import datetime

_price_records = [
    PriceRecord(
        id=uuid4(),
        grocery_item_id=uuid4(),  # Should ideally match an existing GroceryItem id
        market_id=uuid4(),  # Should ideally match an existing Market id
        price=1.99,
        date_recorded=datetime.utcnow(),
    ),
    PriceRecord(
        id=uuid4(),
        grocery_item_id=uuid4(),  # Same as above
        market_id=uuid4(),  # Same as above
        price=0.99,
        date_recorded=datetime.utcnow(),
    ),
    PriceRecord(
        id=uuid4(),
        grocery_item_id=uuid4(),  # Same as above
        market_id=uuid4(),  # Same as above
        price=2.99,
        date_recorded=datetime.utcnow(),
    ),
    PriceRecord(
        id=uuid4(),
        grocery_item_id=uuid4(),  # Same as above
        market_id=uuid4(),  # Same as above
        price=3.99,
        date_recorded=datetime.utcnow(),
    ),
]


def get_all() -> list[PriceRecord]:
    return _price_records


def get_by_grocery_item_id(grocery_item_id: UUID) -> list[PriceRecord]:
    return [
        record
        for record in _price_records
        if str(record.grocery_item_id) == grocery_item_id
    ]


def create(price_record: PriceRecord) -> PriceRecord:
    _price_records.append(price_record)
    return price_record


def update(record_id: UUID, updated_record: PriceRecord) -> PriceRecord:
    for i, record in enumerate(_price_records):
        if record.id == record.id:
            _price_records[i] = updated_record
            return updated_record
    return None


def delete(record_id: UUID) -> bool:
    for i, record in enumerate(_price_records):
        if record.id == record_id:
            del _price_records[i]
            return True
    return False
