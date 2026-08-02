import random
from datetime import datetime

from app.schemas.transaction import Transaction
from app.data.customers import CUSTOMERS
from app.data.merchants import MERCHANTS


def generate_transaction():

    customer = random.choice(CUSTOMERS)
    merchant = random.choice(MERCHANTS)

    fraud_score = random.randint(0, 100)
    is_fraud = fraud_score >= 90

    return Transaction(
        transaction_id=f"TXN-{random.randint(100000,999999)}",

        customer_id=customer["id"],
        customer_name=f"{customer['first_name']} {customer['last_name']}",
        issuing_bank=customer["bank"],

        merchant_id=merchant["id"],
        merchant_name=merchant["name"],
        merchant_category=merchant["category"],
        settlement_bank=merchant["settlement_bank"],

        amount=round(random.uniform(20, 5000), 2),
        currency="ZAR",

        payment_method=random.choice(["Visa", "Mastercard"]),

        status=random.choice(["SUCCESS", "FAILED"]),

        gateway=random.choice(["Visa", "Mastercard"]),

        fraud_score=fraud_score,
        is_fraud=is_fraud,

        timestamp=datetime.now()
    )