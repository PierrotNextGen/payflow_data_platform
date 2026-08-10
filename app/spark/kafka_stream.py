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

KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"
KAFKA_TOPIC = "transactions"

spark = (
    SparkSession.builder
    .appName("PayFlowKafkaStream")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


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


# --------------------------------------------------
# Read transactions continuously from Kafka
# --------------------------------------------------

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
    
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
     
    .load()
)


# --------------------------------------------------
# Convert Kafka binary value to JSON
# --------------------------------------------------

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


<<<<<<< HEAD
# Print transactions to the terminal
# Write transactions to the data lake as Parquet

query = (
=======
# --------------------------------------------------
# Bronze Data Lake
# --------------------------------------------------

bronze_path = "/opt/spark-data/lake/bronze/transactions"

bronze_query = (
>>>>>>> 24e422c (Build Kafka consumers for PostgreSQL and data lake)
    transactions_df
    .writeStream
    .format("parquet")
    .outputMode("append")
<<<<<<< HEAD
    .option("path", "/opt/spark-data/transactions")
    .option("checkpointLocation", "/opt/spark-checkpoints/transactions")
=======
    .option(
        "path",
        bronze_path
    )
    .option(
        "checkpointLocation",
        "/opt/spark-data/checkpoints/bronze_transactions"
    )
>>>>>>> 24e422c (Build Kafka consumers for PostgreSQL and data lake)
    .start()
)


print("========================================")
print("PayFlow Spark Streaming Started")
print("========================================")
print("Kafka topic:", KAFKA_TOPIC)
print("Bronze data lake:", bronze_path)
print("========================================")


bronze_query.awaitTermination()