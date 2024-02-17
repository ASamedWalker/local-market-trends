from fastapi import FastAPI
from web.trends import router as trends_router
from web.deals import router as deals_router

app = FastAPI()

# Include the routers
app.include_router(trends_router, prefix="/api/v1")
app.include_router(deals_router, prefix="/api/v1")

# Continue with application setup...
