from fastapi import FastAPI
from web.listings import router as listings_router
from web.market_trends import router as market_trends_router
from contextlib import asynccontextmanager
from data.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Place startup logic here
    print("Application starting up...")
    # Your startup code, e.g., database initialization
    init_db()
    yield  # The point at which the app is running
    # Place shutdown logic here
    print("Application shutting down...")
    # Your cleanup code, e.g., closing database connections


app = FastAPI(lifespan=lifespan)


app.include_router(listings_router)
app.include_router(market_trends_router)
