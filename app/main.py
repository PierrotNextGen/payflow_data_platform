from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.api.analytics_router import router as analytics_router
from app.exceptions import AnalyticsDatabaseError


app = FastAPI(
    title="PayFlow API",
    version="1.0.0",
    description="Mock payment processing API for the PayFlow Data Platform"
)


@app.exception_handler(AnalyticsDatabaseError)
async def analytics_database_error_handler(
    request: Request,
    exc: AnalyticsDatabaseError
):
    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc)
        }
    )


app.include_router(router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "PayFlow API"
    }