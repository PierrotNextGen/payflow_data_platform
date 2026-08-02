from datetime import datetime
from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: str

    # Customer
    customer_id: str
    customer_name: str
    customer_age: int
    customer_occupation: str
    customer_segment: str
    customer_city: str
    customer_province: str
    issuing_bank: str

    # Merchant
    merchant_id: str
    merchant_name: str
    merchant_category: str
    merchant_city: str
    merchant_province: str
    settlement_bank: str

    # Transaction
    amount: float
    currency: str
    payment_method: str
    status: str
    gateway: str

    # Fraud
    fraud_score: int
    is_fraud: bool

    # Event Time
    timestamp: datetime