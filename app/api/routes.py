from fastapi import APIRouter

from app.services.transaction_service import generate_transaction

router = APIRouter()


from app.schemas.transaction import Transaction

@router.get("/transactions", response_model=Transaction)
def get_transaction():
    return generate_transaction()