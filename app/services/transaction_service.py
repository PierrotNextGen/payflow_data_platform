import random
from datetime import datetime
import uuid

from app.schemas.transaction import Transaction
from app.data.customers import CUSTOMERS
from app.data.merchants import MERCHANTS


def generate_transaction():

    customer = random.choice(CUSTOMERS)
    merchant = random.choice(MERCHANTS)

    # -----------------------------
    # Customer spending profile
    # -----------------------------
    average = customer["average_transaction"]

    if customer["segment"] == "Premium":
        average *= 2
    elif customer["segment"] == "Business":
        average *= 3

    # -----------------------------
    # Merchant average basket
    # -----------------------------
    merchant_average = merchant["average_basket"]

    amount = round(
        random.uniform(
            min(average, merchant_average) * 0.8,
            max(average, merchant_average) * 1.5
        ),
        2
    )

    # -----------------------------
    # Preferred payment method
    # -----------------------------
    payment_method = customer["preferred_payment"]

    if random.random() < 0.10:
        payment_method = (
            "Visa"
            if payment_method == "Mastercard"
            else "Mastercard"
        )

    # -----------------------------
    # Transaction status
    # -----------------------------
    status = random.choices(
        ["SUCCESS", "FAILED"],
        weights=[95, 5]
    )[0]

    # -----------------------------
    # Gateway
    # -----------------------------
    gateway = payment_method

    # -----------------------------
    # Rule-Based Fraud Detection
    # -----------------------------
    fraud_score = 0

    if amount > average * 2:
        fraud_score += 30

    if merchant["risk_level"] == "HIGH":
        fraud_score += 25
    elif merchant["risk_level"] == "MEDIUM":
        fraud_score += 10

    if customer["risk_rating"] == "HIGH":
        fraud_score += 25
    elif customer["risk_rating"] == "MEDIUM":
        fraud_score += 10

    if payment_method != customer["preferred_payment"]:
        fraud_score += 15

    if status == "FAILED":
        fraud_score += 5

    fraud_score += random.randint(0, 10)
    fraud_score = min(fraud_score, 100)

    is_fraud = fraud_score >= 50

    return Transaction(
        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",

        # Customer
        customer_id=customer["id"],
        customer_name=f"{customer['first_name']} {customer['last_name']}",
        customer_age=customer["age"],
        customer_occupation=customer["occupation"],
        customer_segment=customer["segment"],
        customer_city=customer["city"],
        customer_province=customer["province"],
        issuing_bank=customer["bank"],

        # Merchant
        merchant_id=merchant["id"],
        merchant_name=merchant["name"],
        merchant_category=merchant["category"],
        merchant_city=merchant["city"],
        merchant_province=merchant["province"],
        settlement_bank=merchant["settlement_bank"],

        # Transaction
        amount=amount,
        currency="ZAR",
        payment_method=payment_method,
        status=status,
        gateway=gateway,

        # Fraud
        fraud_score=fraud_score,
        is_fraud=is_fraud,

        # Timestamp
        timestamp=datetime.now()
    )
def generate_transactions(count: int):
    transactions = []

    for _ in range(count):
        transactions.append(generate_transaction())

    return transactions