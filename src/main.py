from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.web import (
    grocery_item,
    market,
    price_record,
    special_offer,
    read_session,
    test_create_grocery_item,
)
from src.data.database import create_db_and_tables


# Assuming you have a hypothetical function to load and unload resources
def load_resources():
    print("Loading resources...")
    # Code to load your resources, e.g., ML models, database connections, etc.


def unload_resources():
    print("Unloading resources...")
    # Code to unload/cleanup resources


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    create_db_and_tables()
    load_resources()  # Load resources at startup
    yield  # Wait for the app to run
    unload_resources()  # Cleanup resources at shutdown


app = FastAPI(lifespan=app_lifespan)


app.include_router(grocery_item.router)
app.include_router(market.router)
app.include_router(price_record.router)
app.include_router(special_offer.router)
app.include_router(read_session.router)
app.include_router(test_create_grocery_item.router)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
