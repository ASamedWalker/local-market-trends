from fastapi import FastAPI
from web import listing

app = FastAPI()

app.include_router(listing.router)