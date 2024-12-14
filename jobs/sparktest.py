from pyspark.sql import SparkSession
spark = (
    SparkSession.builder \
                .master("local")
                .appName("World Count")
                .getOrCreate()
)

#file_path = "/opt/spark/data"