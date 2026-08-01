from datetime import datetime
from faker import Faker
import random

from app.schemas.transaction import Transaction

fake = Faker()

PAYMENT_METHODS = [
    "Card",
    "EFT",
    "Apple Pay",
    "Google Pay"
]

STATUSES = [
    "SUCCESS",
    "FAILED",
    "PENDING"
]

GATEWAYS = [
    "Visa",
    "Mastercard",
    "PayShap"
]


def generate_transaction():
    return Transaction(
        transaction_id=f"TXN-{random.randint(100000,999999)}",
        merchant_id=f"MER-{random.randint(1000,9999)}",
        customer_id=f"CUS-{random.randint(10000,99999)}",
        amount=round(random.uniform(20, 5000), 2),
        currency="ZAR",
        payment_method=random.choice(PAYMENT_METHODS),
        status=random.choice(STATUSES),
        gateway=random.choice(GATEWAYS),
        timestamp=datetime.utcnow()
    )