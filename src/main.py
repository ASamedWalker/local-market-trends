from fastapi import FastAPI
from fastapi.routing import Lifespan
from src.web import (
    grocery_item,
    market,
    price_record,
    special_offer,
    read_session,
)
from src.data.database import create_db_and_tables

app = FastAPI()


@app.router.lifespan()
def on_startup(lifespan: Lifespan):
    create_db_and_tables()


app.include_router(grocery_item.router)
app.include_router(market.router)
app.include_router(price_record.router)
app.include_router(special_offer.router)
app.include_router(read_session.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
