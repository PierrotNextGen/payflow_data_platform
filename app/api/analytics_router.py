from fastapi import APIRouter

from app.analytics.repository import (
    get_summary,
    get_bank_summary,
    get_merchant_summary,
    get_fraud_summary,
    get_province_summary,
)

router = APIRouter()


@router.get("/analytics/summary")
def analytics_summary():
    return get_summary()

@router.get("/analytics/banks")
def analytics_banks():
    return get_bank_summary()

@router.get("/analytics/merchants")
def analytics_merchants():
    return get_merchant_summary()

@router.get("/analytics/fraud")
def analytics_fraud():
    return get_fraud_summary()


@router.get("/analytics/provinces")
def analytics_provinces():
    return get_province_summary()