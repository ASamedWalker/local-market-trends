from fastapi import FastAPI
from web import grocery_item, market, price_record

app = FastAPI()

app.include_router(grocery_item.router)
app.include_router(market.router)
app.include_router(price_record.router)
