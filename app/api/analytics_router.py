from fastapi import APIRouter

from app.analytics.repository import get_summary

router = APIRouter()


@router.get("/analytics/summary")
def analytics_summary():
    return get_summary()