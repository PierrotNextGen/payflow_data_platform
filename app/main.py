from fastapi import FastAPI

from app.api.routes import router
from app.api.analytics_router import router as analytics_router
app = FastAPI(
    title="PayFlow API",
    version="1.0.0",
    description="Mock payment processing API for the PayFlow Data Platform"
)

app.include_router(router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "PayFlow API"
    }