from model.price_record import PriceRecord
from uuid import uuid4
from datetime import datetime

price_records = [
    PriceRecord(id=uuid4(), item_id=uuid4(), price=1.99, date=datetime.now()),
    PriceRecord(id=uuid4(), item_id=uuid4(), price=0.99, date=datetime.now()),
    PriceRecord(id=uuid4(), item_id=uuid4(), price=2.49, date=datetime.now()),
    PriceRecord(id=uuid4(), item_id=uuid4(), price=3.00, date=datetime.now()),
]