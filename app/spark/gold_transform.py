from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# ============================================================
# PayFlow Gold Transformation
# ============================================================

print("========================================")
print("PayFlow Gold Transformation")
print("========================================")


# ============================================================
# Spark Session
# ============================================================

spark = (
    SparkSession.builder
    .appName("PayFlowGoldTransformation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# Paths
# ============================================================

silver_path = "/opt/spark-data/lake/silver/transactions"
gold_path = "/opt/spark-data/lake/gold"


print(f"Silver path: {silver_path}")
print(f"Gold path: {gold_path}")
print("========================================")


# ============================================================
# Read Silver Data
# ============================================================

print("Reading Silver data...")

silver_df = spark.read.parquet(silver_path)

print("Silver schema:")
silver_df.printSchema()

silver_count = silver_df.count()

print(f"Silver records: {silver_count}")


if silver_count == 0:
    raise ValueError("Silver layer contains no records.")


# ============================================================
# Prepare Gold Data
# ============================================================

print("Preparing Gold data...")


gold_base = (
    silver_df
    .withColumn(
        "transaction_date",
        F.to_date(F.col("timestamp"))
    )
    .withColumn(
        "transaction_hour",
        F.hour(F.col("timestamp"))
    )
    .withColumn(
        "transaction_amount_category",
        F.when(F.col("amount") < 500, "LOW")
        .when(F.col("amount") < 2000, "MEDIUM")
        .when(F.col("amount") < 5000, "HIGH")
        .otherwise("VERY_HIGH")
    )
    .withColumn(
        "fraud_status",
        F.when(F.col("is_fraud") == True, "FRAUD")
        .otherwise("LEGITIMATE")
    )
)


# ============================================================
# Gold Dataset 1
# Daily Transaction Summary
# ============================================================

print("Creating daily transaction summary...")

daily_transaction_summary = (
    gold_base
    .groupBy(
        "transaction_date",
        "currency"
    )
    .agg(
        F.count("*").alias("transaction_count"),

        F.round(
            F.sum("amount"),
            2
        ).alias("total_transaction_amount"),

        F.round(
            F.avg("amount"),
            2
        ).alias("average_transaction_amount"),

        F.round(
            F.max("amount"),
            2
        ).alias("maximum_transaction_amount"),

        F.round(
            F.min("amount"),
            2
        ).alias("minimum_transaction_amount"),

        F.sum(
            F.when(
                F.col("status") == "SUCCESS",
                1
            ).otherwise(0)
        ).alias("successful_transactions"),

        F.sum(
            F.when(
                F.col("status") == "FAILED",
                1
            ).otherwise(0)
        ).alias("failed_transactions"),

        F.sum(
            F.when(
                F.col("is_fraud") == True,
                1
            ).otherwise(0)
        ).alias("fraudulent_transactions"),

        F.round(
            F.avg("fraud_score"),
            2
        ).alias("average_fraud_score")
    )
)


# ============================================================
# Gold Dataset 2
# Merchant Performance
# ============================================================

print("Creating merchant performance dataset...")

merchant_performance = (
    gold_base
    .groupBy(
        "merchant_id",
        "merchant_name",
        "merchant_category",
        "merchant_city",
        "merchant_province",
        "currency"
    )
    .agg(
        F.count("*").alias("transaction_count"),

        F.round(
            F.sum("amount"),
            2
        ).alias("total_transaction_amount"),

        F.round(
            F.avg("amount"),
            2
        ).alias("average_transaction_amount"),

        F.sum(
            F.when(
                F.col("status") == "SUCCESS",
                1
            ).otherwise(0)
        ).alias("successful_transactions"),

        F.sum(
            F.when(
                F.col("status") == "FAILED",
                1
            ).otherwise(0)
        ).alias("failed_transactions"),

        F.sum(
            F.when(
                F.col("is_fraud") == True,
                1
            ).otherwise(0)
        ).alias("fraudulent_transactions"),

        F.round(
            F.avg("fraud_score"),
            2
        ).alias("average_fraud_score"),

        F.round(
            F.max("amount"),
            2
        ).alias("maximum_transaction_amount")
    )
)


# ============================================================
# Gold Dataset 3
# Fraud Analysis
# ============================================================

print("Creating fraud analysis dataset...")

fraud_analysis = (
    gold_base
    .groupBy(
        "transaction_date",
        "merchant_category",
        "payment_method",
        "fraud_status",
        "currency"
    )
    .agg(
        F.count("*").alias("transaction_count"),

        F.round(
            F.sum("amount"),
            2
        ).alias("total_transaction_amount"),

        F.round(
            F.avg("amount"),
            2
        ).alias("average_transaction_amount"),

        F.round(
            F.avg("fraud_score"),
            2
        ).alias("average_fraud_score"),

        F.round(
            F.max("fraud_score"),
            2
        ).alias("maximum_fraud_score"),

        F.round(
            F.min("fraud_score"),
            2
        ).alias("minimum_fraud_score")
    )
)


# ============================================================
# Gold Data Quality Checks
# ============================================================

print("Running Gold data quality checks...")


invalid_amounts = gold_base.filter(
    F.col("amount").isNull()
    | (F.col("amount") < 0)
).count()


invalid_timestamps = gold_base.filter(
    F.col("timestamp").isNull()
).count()


invalid_transaction_ids = gold_base.filter(
    F.col("transaction_id").isNull()
).count()


if invalid_amounts > 0:
    raise ValueError(
        f"Gold data quality check failed: "
        f"{invalid_amounts} invalid transaction amounts found."
    )


if invalid_timestamps > 0:
    raise ValueError(
        f"Gold data quality check failed: "
        f"{invalid_timestamps} NULL timestamps found."
    )


if invalid_transaction_ids > 0:
    raise ValueError(
        f"Gold data quality check failed: "
        f"{invalid_transaction_ids} NULL transaction IDs found."
    )


print("Gold data quality checks passed.")


# ============================================================
# Show Gold Results
# ============================================================

print()
print("========================================")
print("Daily Transaction Summary")
print("========================================")

daily_transaction_summary.show(
    20,
    truncate=False
)


print()
print("========================================")
print("Merchant Performance")
print("========================================")

merchant_performance.show(
    20,
    truncate=False
)


print()
print("========================================")
print("Fraud Analysis")
print("========================================")

fraud_analysis.show(
    20,
    truncate=False
)


# ============================================================
# Write Gold Data
# ============================================================

print()
print("Writing Gold data...")


# ------------------------------------------------------------
# Daily transaction summary
# ------------------------------------------------------------

(
    daily_transaction_summary
    .write
    .mode("overwrite")
    .partitionBy("transaction_date")
    .parquet(
        f"{gold_path}/daily_transactions"
    )
)


# ------------------------------------------------------------
# Merchant performance
# ------------------------------------------------------------

(
    merchant_performance
    .write
    .mode("overwrite")
    .parquet(
        f"{gold_path}/merchant_performance"
    )
)


# ------------------------------------------------------------
# Fraud analysis
# ------------------------------------------------------------

(
    fraud_analysis
    .write
    .mode("overwrite")
    .partitionBy("transaction_date")
    .parquet(
        f"{gold_path}/fraud_analysis"
    )
)


# ============================================================
# Completion
# ============================================================

print()
print("========================================")
print("Gold transformation completed")
print("========================================")

print(f"Gold data lake: {gold_path}")

print()
print("Gold datasets created:")

print("1. daily_transactions")
print("2. merchant_performance")
print("3. fraud_analysis")

print("========================================")


# ============================================================
# Stop Spark
# ============================================================

spark.stop()