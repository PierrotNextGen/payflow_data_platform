from fastapi import APIRouter

from app.analytics.repository import (
    get_daily_transactions,
    get_merchant_summary,
    get_fraud_summary,
)

from app.schemas.analytics import (
    DailyTransactionResponse,
    MerchantPerformanceResponse,
    FraudAnalysisResponse,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/daily",
    response_model=list[DailyTransactionResponse],
    summary="Get daily transaction analytics",
    description=(
        "Returns daily transaction performance metrics from the "
        "PayFlow Gold analytics layer."
    ),
)
def analytics_daily():
    return get_daily_transactions()


@router.get(
    "/merchants",
    response_model=list[MerchantPerformanceResponse],
    summary="Get merchant performance analytics",
    description=(
        "Returns transaction volume, success rates, fraud metrics, "
        "and transaction amounts aggregated by merchant."
    ),
)
def analytics_merchants():
    return get_merchant_summary()


@router.get(
    "/fraud",
    response_model=list[FraudAnalysisResponse],
    summary="Get fraud analytics",
    description=(
        "Returns fraud analysis aggregated by merchant category, "
        "payment method, fraud status, currency, and transaction date."
    ),
)
def analytics_fraud():
    return get_fraud_summary()