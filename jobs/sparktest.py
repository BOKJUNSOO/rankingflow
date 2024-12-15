from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from datetime import datetime 
spark = (
    SparkSession.builder \
                .master("local")
                .appName("submit_test")
                .getOrCreate()
)
target_date = datetime.now().strftime("%Y-%m-%d")

file_path = f"/opt/bitnami/spark/data/ranking_{target_date}.json"
print(f"{file_path}")
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