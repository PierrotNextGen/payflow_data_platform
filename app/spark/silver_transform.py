
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    round as spark_round,
    when,
    to_timestamp,
)
from pyspark.sql.types import (
    StringType,
    IntegerType,
    DoubleType,
    BooleanType,
    TimestampType,
)


# ============================================================
# PayFlow Data Platform
# Silver Layer Transformation
# ============================================================

BRONZE_PATH = "/opt/spark-data/lake/bronze/transactions"
SILVER_PATH = "/opt/spark-data/lake/silver/transactions"


# ============================================================
# Spark Session
# ============================================================

spark = (
    SparkSession.builder
    .appName("PayFlowSilverTransform")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# Startup Information
# ============================================================

print("========================================")
print("PayFlow Silver Transformation")
print("========================================")
print("Bronze path:", BRONZE_PATH)
print("Silver path:", SILVER_PATH)
print("========================================")


# ============================================================
# Read Bronze Data
# ============================================================

print("Reading Bronze data...")

bronze_df = (
    spark.read
    .parquet(BRONZE_PATH)
)

print("Bronze schema:")
bronze_df.printSchema()


bronze_count = bronze_df.count()

print(f"Bronze records: {bronze_count}")


# ============================================================
# Silver Transformation
# ============================================================

print("Transforming Bronze data into Silver...")


silver_df = (
    bronze_df

    # --------------------------------------------------------
    # Clean string fields
    # --------------------------------------------------------

    .withColumn(
        "transaction_id",
        trim(col("transaction_id"))
    )

    .withColumn(
        "customer_id",
        trim(col("customer_id"))
    )

    .withColumn(
        "customer_name",
        trim(col("customer_name"))
    )

    .withColumn(
        "customer_occupation",
        trim(col("customer_occupation"))
    )

    .withColumn(
        "customer_segment",
        trim(col("customer_segment"))
    )

    .withColumn(
        "customer_city",
        trim(col("customer_city"))
    )

    .withColumn(
        "customer_province",
        trim(col("customer_province"))
    )

    .withColumn(
        "issuing_bank",
        trim(col("issuing_bank"))
    )

    .withColumn(
        "merchant_id",
        trim(col("merchant_id"))
    )

    .withColumn(
        "merchant_name",
        trim(col("merchant_name"))
    )

    .withColumn(
        "merchant_category",
        trim(col("merchant_category"))
    )

    .withColumn(
        "merchant_city",
        trim(col("merchant_city"))
    )

    .withColumn(
        "merchant_province",
        trim(col("merchant_province"))
    )

    .withColumn(
        "settlement_bank",
        trim(col("settlement_bank"))
    )

    .withColumn(
        "currency",
        trim(col("currency"))
    )

    .withColumn(
        "payment_method",
        trim(col("payment_method"))
    )

    .withColumn(
        "status",
        trim(col("status"))
    )

    .withColumn(
        "gateway",
        trim(col("gateway"))
    )

    # --------------------------------------------------------
    # Standardize categorical fields
    # --------------------------------------------------------

    .withColumn(
        "currency",
        upper(col("currency"))
    )

    .withColumn(
        "payment_method",
        upper(col("payment_method"))
    )

    .withColumn(
        "status",
        upper(col("status"))
    )

    .withColumn(
        "gateway",
        upper(col("gateway"))
    )

    .withColumn(
        "customer_segment",
        upper(col("customer_segment"))
    )

    # --------------------------------------------------------
    # Standardize amount
    # --------------------------------------------------------

    .withColumn(
        "amount",
        spark_round(col("amount"), 2)
    )

    # --------------------------------------------------------
    # Validate transaction amount
    # --------------------------------------------------------

    .withColumn(
        "amount",
        when(
            col("amount") >= 0,
            col("amount")
        ).otherwise(None)
    )

    # --------------------------------------------------------
    # Validate customer age
    # --------------------------------------------------------

    .withColumn(
        "customer_age",
        when(
            (col("customer_age") >= 18)
            & (col("customer_age") <= 100),
            col("customer_age")
        ).otherwise(None)
    )

    # --------------------------------------------------------
    # Normalize transaction status
    # --------------------------------------------------------

    .withColumn(
        "status",
        when(
            col("status").isin("SUCCESS", "FAILED"),
            col("status")
        ).otherwise("UNKNOWN")
    )

    # --------------------------------------------------------
    # Normalize payment method
    # --------------------------------------------------------

    .withColumn(
        "payment_method",
        when(
            col("payment_method").isin(
                "VISA",
                "MASTERCARD",
                "CASH",
                "MOBILE_MONEY",
                "BANK_TRANSFER"
            ),
            col("payment_method")
        ).otherwise("OTHER")
    )

    # --------------------------------------------------------
    # Validate fraud score
    # --------------------------------------------------------

    .withColumn(
        "fraud_score",
        when(
            col("fraud_score") < 0,
            0
        )
        .when(
            col("fraud_score") > 100,
            100
        )
        .otherwise(col("fraud_score"))
    )

    # --------------------------------------------------------
    # Recalculate fraud flag
    #
    # Our PayFlow fraud threshold is 50.
    # --------------------------------------------------------

    .withColumn(
        "is_fraud",
        when(
            col("fraud_score") >= 50,
            True
        ).otherwise(False)
    )

    # --------------------------------------------------------
    # Ensure timestamp is TimestampType
    # --------------------------------------------------------

    .withColumn(
        "timestamp",
        col("timestamp").cast(TimestampType())
    )

    # --------------------------------------------------------
    # Remove records missing required identifiers
    # --------------------------------------------------------

    .filter(
        col("transaction_id").isNotNull()
        & (col("transaction_id") != "")
        & col("customer_id").isNotNull()
        & (col("customer_id") != "")
        & col("merchant_id").isNotNull()
        & (col("merchant_id") != "")
    )

    # --------------------------------------------------------
    # Remove duplicate transactions
    # --------------------------------------------------------

    .dropDuplicates(
        ["transaction_id"]
    )
)


# ============================================================
# Silver Data Quality Checks
# ============================================================

print("Running Silver data quality checks...")


silver_count = silver_df.count()

null_transaction_ids = (
    silver_df
    .filter(col("transaction_id").isNull())
    .count()
)

invalid_amounts = (
    silver_df
    .filter(col("amount") < 0)
    .count()
)

invalid_fraud_scores = (
    silver_df
    .filter(
        (col("fraud_score") < 0)
        | (col("fraud_score") > 100)
    )
    .count()
)


print("----------------------------------------")
print("Silver Data Quality Results")
print("----------------------------------------")
print("Bronze records:", bronze_count)
print("Silver records:", silver_count)
print("Null transaction IDs:", null_transaction_ids)
print("Invalid amounts:", invalid_amounts)
print("Invalid fraud scores:", invalid_fraud_scores)
print("----------------------------------------")


if null_transaction_ids > 0:
    raise ValueError(
        "Silver quality check failed: "
        "NULL transaction IDs found."
    )


if invalid_amounts > 0:
    raise ValueError(
        "Silver quality check failed: "
        "negative transaction amounts found."
    )


if invalid_fraud_scores > 0:
    raise ValueError(
        "Silver quality check failed: "
        "fraud scores outside 0-100 range."
    )


print("Silver data quality checks passed.")


# ============================================================
# Silver Schema
# ============================================================

print("Silver schema:")

silver_df.printSchema()


# ============================================================
# Preview Silver Data
# ============================================================

print("Silver data preview:")

silver_df.show(
    10,
    truncate=False
)


# ============================================================
# Write Silver Data
# ============================================================

print("Writing Silver data...")

(
    silver_df
    .write
    .mode("overwrite")
    .parquet(SILVER_PATH)
)


# ============================================================
# Completion
# ============================================================

print("========================================")
print("Silver transformation completed")
print("========================================")
print("Records written:", silver_count)
print("Silver path:", SILVER_PATH)
print("========================================")


spark.stop()
