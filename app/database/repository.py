from app.database.connection import get_connection


INSERT_QUERY = """
INSERT INTO transactions (
    transaction_id,
    customer_id,
    customer_name,
    customer_age,
    customer_occupation,
    customer_segment,
    customer_city,
    customer_province,
    issuing_bank,
    merchant_id,
    merchant_name,
    merchant_category,
    merchant_city,
    merchant_province,
    settlement_bank,
    amount,
    currency,
    payment_method,
    status,
    gateway,
    fraud_score,
    is_fraud,
    timestamp
)
VALUES (
    %(transaction_id)s,
    %(customer_id)s,
    %(customer_name)s,
    %(customer_age)s,
    %(customer_occupation)s,
    %(customer_segment)s,
    %(customer_city)s,
    %(customer_province)s,
    %(issuing_bank)s,
    %(merchant_id)s,
    %(merchant_name)s,
    %(merchant_category)s,
    %(merchant_city)s,
    %(merchant_province)s,
    %(settlement_bank)s,
    %(amount)s,
    %(currency)s,
    %(payment_method)s,
    %(status)s,
    %(gateway)s,
    %(fraud_score)s,
    %(is_fraud)s,
    %(timestamp)s
);
"""


def save_transaction(transaction):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(INSERT_QUERY, transaction.model_dump())

    conn.commit()

    cur.close()
    conn.close()


def save_transactions(transactions):
    conn = get_connection()
    cur = conn.cursor()

    data = [transaction.model_dump() for transaction in transactions]

    cur.executemany(INSERT_QUERY, data)

    conn.commit()

    cur.close()
    conn.close()