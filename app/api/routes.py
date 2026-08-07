from fastapi import APIRouter

from app.schemas.transaction import Transaction
from app.services.transaction_service import (
    generate_transaction,
    generate_transactions,
)

router = APIRouter()


@router.get("/transactions", response_model=Transaction)
def get_transaction():
    return generate_transaction()


@router.post("/transactions/generate")
def generate_bulk_transactions(count: int = 1000):

    transactions = generate_transactions(count)

    return {
        "generated": len(transactions),
        "published": len(transactions),
    }