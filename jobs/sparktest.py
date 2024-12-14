from pyspark.sql import SparkSession
spark = (
    SparkSession.builder \
                .master("local")
                .appName("World Count")
                .getOrCreate()
)
file_path = "/opt/bitnami/spark/data/ranking_2024-12-14.json"
df = spark.read.json(f"{file_path}")
df.printSchema()