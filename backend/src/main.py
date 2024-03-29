from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from web import (
    grocery_item,
    market,
    price_record,
    special_offer,
)
from data.database import create_db_and_tables
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


# Assuming you have a hypothetical function to load and unload resources
def load_resources():
    print("Loading resources...")
    # Code to load your resources, e.g. database connections, etc.


def unload_resources():
    print("Unloading resources...")
    # Code to unload/cleanup resources


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await create_db_and_tables()
    load_resources()  # Load resources at startup
    yield  # Wait for the app to run
    unload_resources()  # Cleanup resources at shutdown


app = FastAPI(lifespan=app_lifespan)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static/images/"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    # Log the error or send it to an error tracking system
    logger.error(f"SQLAlchemyError occurred: {exc}")
    return HTTPException(status_code=500, detail="A database error occurred")


app.include_router(grocery_item.router)
app.include_router(market.router)
app.include_router(price_record.router)
app.include_router(special_offer.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
