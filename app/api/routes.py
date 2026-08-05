from fastapi import APIRouter

from app.schemas.transaction import Transaction
from app.services.transaction_service import (
    generate_transaction,
    generate_transactions,
)
from app.database.repository import (
    save_transaction,
    save_transactions,
)

router = APIRouter()


@router.get("/transactions", response_model=Transaction)
def get_transaction():
    transaction = generate_transaction()
    save_transaction(transaction)
    return transaction


@router.post("/transactions/generate")
def generate_bulk_transactions(count: int = 1000):
    transactions = generate_transactions(count)

    save_transactions(transactions)

    return {
        "generated": len(transactions),
        "saved": len(transactions),
    }