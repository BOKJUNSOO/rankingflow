from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import datetime

spark = (
    SparkSession.builder \
                .master("local")
                .appName("submit_test")
                .getOrCreate()
)

now = datetime.datetime.now()# airflow UTC 로 인식(9시간이 느리다)
#target_date = now + datetime.timedelta(days=1) # 스케줄은 한국시간 01:00에 시작
target_date = now.strftime("%Y-%m-%d")
print(f"{target_date}일자의 data를 정제합니다.")
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