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