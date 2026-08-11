from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("VerifyPayFlowGold")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

base = "/opt/spark-data/lake/gold"

for name in [
    "daily_transactions",
    "merchant_performance",
    "fraud_analysis"
]:
    print("\n========================================")
    print(name)
    print("========================================")

    df = spark.read.parquet(f"{base}/{name}")

    print("Schema:")
    df.printSchema()

    print("Records:", df.count())

    print("Data:")
    df.show(20, truncate=False)

spark.stop()