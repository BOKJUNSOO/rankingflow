from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import datetime
from common.get_data import get_data
spark = (
    SparkSession.builder \
                .master("local")
                .appName("submit_test")
                .getOrCreate()
)

# UTC time
UTC = datetime.datetime.now()
# Korea TZ
target_date = UTC + datetime.timedelta(hours=9)
target_date = target_date.strftime('%Y-%m-%d')

print(f"{target_date}일자의 data를 정제합니다.")
# 특정 일자의 data가 없으면 common fuction 호출해서 데이터 수집하기
file_path = f"/opt/airflow/data/ranking_{target_date}.json"

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