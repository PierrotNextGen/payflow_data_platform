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


# Read transactions continuously from Kafka
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)


# Kafka value is binary.
# Convert it to a string and parse the JSON.
transactions_df = (
    kafka_df
    .selectExpr("CAST(value AS STRING) AS json_value")
    .select(
        from_json(col("json_value"), transaction_schema).alias("transaction")
    )
    .select("transaction.*")
)


# Print transactions to the terminal
query = (
    transactions_df
    .writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .option("numRows", 20)
    .start()
)


print("Spark streaming from Kafka...")
print("Topic:", KAFKA_TOPIC)

query.awaitTermination()