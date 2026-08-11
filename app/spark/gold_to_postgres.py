from pyspark.sql import SparkSession


# ============================================================
# PayFlow Gold -> PostgreSQL
# ============================================================

GOLD_BASE_PATH = "/opt/spark-data/lake/gold"

POSTGRES_URL = "jdbc:postgresql://postgres:5432/payflow"
POSTGRES_USER = "payflow"
POSTGRES_PASSWORD = "postgres"

JDBC_PROPERTIES = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}


def write_to_postgres(df, table_name):
    print(f"Writing {table_name} to PostgreSQL...")

    df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", table_name) \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .option("numPartitions", "1") \
        .mode("overwrite") \
        .save()

    print(f"{table_name} written successfully.")


def main():

    print("=" * 50)
    print("PayFlow Gold -> PostgreSQL")
    print("=" * 50)

    spark = (
        SparkSession.builder
        .appName("PayFlow-Gold-To-PostgreSQL")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # --------------------------------------------------------
    # Read Gold datasets
    # --------------------------------------------------------

    print("\nReading Gold datasets...")

    daily_transactions = spark.read.parquet(
        f"{GOLD_BASE_PATH}/daily_transactions"
    )

    merchant_performance = spark.read.parquet(
        f"{GOLD_BASE_PATH}/merchant_performance"
    )

    fraud_analysis = spark.read.parquet(
        f"{GOLD_BASE_PATH}/fraud_analysis"
    )

    print("\nGold record counts:")

    print(
        f"daily_transactions: {daily_transactions.count()}"
    )

    print(
        f"merchant_performance: {merchant_performance.count()}"
    )

    print(
        f"fraud_analysis: {fraud_analysis.count()}"
    )

    # --------------------------------------------------------
    # Write to PostgreSQL
    # --------------------------------------------------------

    print("\nWriting Gold data to PostgreSQL...")

    write_to_postgres(
        daily_transactions,
        "daily_transactions"
    )

    write_to_postgres(
        merchant_performance,
        "merchant_performance"
    )

    write_to_postgres(
        fraud_analysis,
        "fraud_analysis"
    )

    print("\n" + "=" * 50)
    print("Gold -> PostgreSQL completed successfully.")
    print("=" * 50)

    spark.stop()


if __name__ == "__main__":
    main()