from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    BooleanType,
    TimestampType,
)


# ==================================================
# Kafka Configuration
# ==================================================

KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"
KAFKA_TOPIC = "transactions"


# ==================================================
# Spark Session
# ==================================================

spark = (
    SparkSession.builder
    .appName("PayFlowKafkaStream")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ==================================================
# Transaction Schema
# ==================================================

transaction_schema = StructType([
    StructField("transaction_id", StringType(), True),

    StructField("customer_id", StringType(), True),
    StructField("customer_name", StringType(), True),
    StructField("customer_age", IntegerType(), True),
    StructField("customer_occupation", StringType(), True),
    StructField("customer_segment", StringType(), True),
    StructField("customer_city", StringType(), True),
    StructField("customer_province", StringType(), True),
    StructField("issuing_bank", StringType(), True),

    StructField("merchant_id", StringType(), True),
    StructField("merchant_name", StringType(), True),
    StructField("merchant_category", StringType(), True),
    StructField("merchant_city", StringType(), True),
    StructField("merchant_province", StringType(), True),
    StructField("settlement_bank", StringType(), True),

    StructField("amount", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("payment_method", StringType(), True),
    StructField("status", StringType(), True),
    StructField("gateway", StringType(), True),

    StructField("fraud_score", IntegerType(), True),
    StructField("is_fraud", BooleanType(), True),

    StructField("timestamp", TimestampType(), True),
])


# ==================================================
# Read Transactions Continuously From Kafka
# ==================================================

kafka_df = (
    spark.readStream
    .format("kafka")
    .option(
        "kafka.bootstrap.servers",
        KAFKA_BOOTSTRAP_SERVERS
    )
    .option(
        "subscribe",
        KAFKA_TOPIC
    )
    .option(
        "startingOffsets",
        "earliest"
    )
    .option(
        "failOnDataLoss",
        "false"
    )
    .load()
)


# ==================================================
# Convert Kafka Binary Value To JSON
# ==================================================

transactions_df = (
    kafka_df
    .selectExpr(
        "CAST(value AS STRING) AS json_value"
    )
    .select(
        from_json(
            col("json_value"),
            transaction_schema
        ).alias("transaction")
    )
    .select("transaction.*")
)


# ==================================================
# Bronze Data Lake
# ==================================================

bronze_path = "/opt/spark-data/lake/bronze/transactions"

bronze_checkpoint = (
    "/opt/spark-data/checkpoints/bronze_transactions"
)


bronze_query = (
    transactions_df
    .writeStream
    .format("parquet")
    .outputMode("append")
    .option(
        "path",
        bronze_path
    )
    .option(
        "checkpointLocation",
        bronze_checkpoint
    )
    .start()
)


# ==================================================
# Startup Information
# ==================================================

print("========================================")
print("PayFlow Spark Streaming Started")
print("========================================")
print("Kafka broker:", KAFKA_BOOTSTRAP_SERVERS)
print("Kafka topic:", KAFKA_TOPIC)
print("Bronze data lake:", bronze_path)
print("Checkpoint:", bronze_checkpoint)
print("========================================")


# ==================================================
# Keep Streaming Application Running
# ==================================================

bronze_query.awaitTermination()