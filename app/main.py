from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="PayFlow API",
    version="1.0.0",
    description="Mock payment processing API for the PayFlow Data Platform"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to PayFlow API!"
    }