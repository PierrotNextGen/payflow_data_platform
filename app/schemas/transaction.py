from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str
    merchant_id: str
    customer_id: str
    amount: float
    currency: str
    payment_method: str
    status: str
    gateway: str
    timestamp: datetime