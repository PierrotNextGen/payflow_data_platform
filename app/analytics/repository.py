import psycopg

from app.database.connection import get_connection
from app.exceptions import AnalyticsDatabaseError


def get_daily_transactions():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT
                        currency,
                        transaction_count,
                        total_transaction_amount,
                        average_transaction_amount,
                        maximum_transaction_amount,
                        minimum_transaction_amount,
                        successful_transactions,
                        failed_transactions,
                        fraudulent_transactions,
                        average_fraud_score,
                        transaction_date
                    FROM daily_transactions
                    ORDER BY transaction_date DESC;
                """)

                rows = cur.fetchall()

        results = []

        for row in rows:
            results.append({
                "currency": row["currency"],
                "transaction_count": int(row["transaction_count"]),
                "total_transaction_amount": float(
                    row["total_transaction_amount"]
                ),
                "average_transaction_amount": float(
                    row["average_transaction_amount"]
                ),
                "maximum_transaction_amount": float(
                    row["maximum_transaction_amount"]
                ),
                "minimum_transaction_amount": float(
                    row["minimum_transaction_amount"]
                ),
                "successful_transactions": int(
                    row["successful_transactions"]
                ),
                "failed_transactions": int(
                    row["failed_transactions"]
                ),
                "fraudulent_transactions": int(
                    row["fraudulent_transactions"]
                ),
                "average_fraud_score": float(
                    row["average_fraud_score"]
                ),
                "transaction_date": row["transaction_date"]
            })

        return results

    except psycopg.Error as exc:
        raise AnalyticsDatabaseError(
            "Unable to retrieve daily transaction analytics."
        ) from exc


def get_merchant_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT
                        merchant_id,
                        merchant_name,
                        merchant_category,
                        merchant_city,
                        merchant_province,
                        currency,
                        transaction_count,
                        total_transaction_amount,
                        average_transaction_amount,
                        successful_transactions,
                        failed_transactions,
                        fraudulent_transactions,
                        average_fraud_score,
                        maximum_transaction_amount
                    FROM merchant_performance
                    ORDER BY total_transaction_amount DESC;
                """)

                rows = cur.fetchall()

        results = []

        for row in rows:
            results.append({
                "merchant_id": row["merchant_id"],
                "merchant_name": row["merchant_name"],
                "merchant_category": row["merchant_category"],
                "merchant_city": row["merchant_city"],
                "merchant_province": row["merchant_province"],
                "currency": row["currency"],
                "transaction_count": int(row["transaction_count"]),
                "total_transaction_amount": float(
                    row["total_transaction_amount"]
                ),
                "average_transaction_amount": float(
                    row["average_transaction_amount"]
                ),
                "successful_transactions": int(
                    row["successful_transactions"]
                ),
                "failed_transactions": int(
                    row["failed_transactions"]
                ),
                "fraudulent_transactions": int(
                    row["fraudulent_transactions"]
                ),
                "average_fraud_score": float(
                    row["average_fraud_score"]
                ),
                "maximum_transaction_amount": float(
                    row["maximum_transaction_amount"]
                )
            })

        return results

    except psycopg.Error as exc:
        raise AnalyticsDatabaseError(
            "Unable to retrieve merchant performance analytics."
        ) from exc


def get_fraud_summary():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT
                        merchant_category,
                        payment_method,
                        fraud_status,
                        currency,
                        transaction_count,
                        total_transaction_amount,
                        average_transaction_amount,
                        average_fraud_score,
                        maximum_fraud_score,
                        minimum_fraud_score,
                        transaction_date
                    FROM fraud_analysis
                    ORDER BY transaction_date DESC,
                             total_transaction_amount DESC;
                """)

                rows = cur.fetchall()

        results = []

        for row in rows:
            results.append({
                "merchant_category": row["merchant_category"],
                "payment_method": row["payment_method"],
                "fraud_status": row["fraud_status"],
                "currency": row["currency"],
                "transaction_count": int(row["transaction_count"]),
                "total_transaction_amount": float(
                    row["total_transaction_amount"]
                ),
                "average_transaction_amount": float(
                    row["average_transaction_amount"]
                ),
                "average_fraud_score": float(
                    row["average_fraud_score"]
                ),
                "maximum_fraud_score": float(
                    row["maximum_fraud_score"]
                ),
                "minimum_fraud_score": float(
                    row["minimum_fraud_score"]
                ),
                "transaction_date": row["transaction_date"]
            })

        return results

    except psycopg.Error as exc:
        raise AnalyticsDatabaseError(
            "Unable to retrieve fraud analytics."
        ) from exc