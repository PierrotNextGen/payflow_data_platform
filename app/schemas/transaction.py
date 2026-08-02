from datetime import datetime
from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: str

    customer_id: str
    customer_name: str
    issuing_bank: str

    merchant_id: str
    merchant_name: str
    merchant_category: str
    settlement_bank: str

    amount: float
    currency: str

    payment_method: str

    status: str

    gateway: str

    fraud_score: int
    is_fraud: bool

    timestamp: datetime
    