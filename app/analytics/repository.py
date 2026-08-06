from app.database.connection import get_connection


def get_summary():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_transactions,
            COALESCE(SUM(amount), 0) AS total_volume,
            COALESCE(AVG(amount), 0) AS average_transaction,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_transactions
        FROM transactions;
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_transactions": int(row["total_transactions"]),
        "total_volume": float(row["total_volume"]),
        "average_transaction": round(float(row["average_transaction"]), 2),
        "fraud_transactions": int(row["fraud_transactions"] or 0)
    }

def get_bank_summary():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            issuing_bank,
            COUNT(*) AS transactions,
            COALESCE(SUM(amount), 0) AS total_volume,
            COALESCE(AVG(amount), 0) AS average_amount
        FROM transactions
        GROUP BY issuing_bank
        ORDER BY total_volume DESC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "issuing_bank": row["issuing_bank"],
            "transactions": row["transactions"],
            "total_volume": float(row["total_volume"]),
            "average_amount": round(float(row["average_amount"]), 2)
        })

    return results

def get_merchant_summary():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            merchant_name,
            merchant_category,
            COUNT(*) AS transactions,
            COALESCE(SUM(amount), 0) AS total_volume,
            COALESCE(AVG(amount), 0) AS average_amount
        FROM transactions
        GROUP BY merchant_name, merchant_category
        ORDER BY total_volume DESC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "merchant_name": row["merchant_name"],
            "merchant_category": row["merchant_category"],
            "transactions": row["transactions"],
            "total_volume": float(row["total_volume"]),
            "average_amount": round(float(row["average_amount"]), 2)
        })

    return results

def get_fraud_summary():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_transactions,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_transactions,
            COALESCE(SUM(CASE WHEN is_fraud THEN amount ELSE 0 END), 0) AS fraud_volume,
            COALESCE(AVG(CASE WHEN is_fraud THEN amount END), 0) AS average_fraud_amount
        FROM transactions;
    """)

    row = cur.fetchone()

    cur.close()
    conn.close()

    total = row["total_transactions"]
    fraud = row["fraud_transactions"] or 0

    fraud_rate = 0

    if total > 0:
        fraud_rate = round((fraud / total) * 100, 2)

    return {
        "total_transactions": total,
        "fraud_transactions": fraud,
        "fraud_rate": fraud_rate,
        "fraud_volume": float(row["fraud_volume"]),
        "average_fraud_amount": round(float(row["average_fraud_amount"]), 2)
    }

def get_province_summary():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            customer_province,
            COUNT(*) AS transactions,
            COALESCE(SUM(amount), 0) AS total_volume,
            COALESCE(AVG(amount), 0) AS average_amount
        FROM transactions
        GROUP BY customer_province
        ORDER BY total_volume DESC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for row in rows:
        results.append({
            "province": row["customer_province"],
            "transactions": row["transactions"],
            "total_volume": float(row["total_volume"]),
            "average_amount": round(float(row["average_amount"]), 2)
        })

    return results