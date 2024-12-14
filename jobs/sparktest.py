from pyspark.sql import SparkSession
import pyspark.sql.functions as F
spark = (
    SparkSession.builder \
                .master("local")
                .appName("submit_test")
                .getOrCreate()
)
file_path = "/opt/bitnami/spark/data/ranking_2024-12-14.json"
df = spark.read \
          .format("json") \
          .option("multiLine", True) \
          .option("header", True) \
          .load(f"{file_path}")
df = df.select(F.explode("ranking")
                         .alias("ranking_info"))
df = df.select("ranking_info.date",
                   "ranking_info.character_name",
                   "ranking_info.character_level",
                   "ranking_info.character_exp",
                   "ranking_info.class_name",
                   "ranking_info.sub_class_name")
df.printSchema()

df.show()