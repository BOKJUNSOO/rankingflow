import pyspark.sql.functions as F

class BaseFilter:
    def __init__(self,spark):
        self.spark = spark
    def filter():
        pass

# 생성한 sparkdataframe을 정제해주는 함수(func)에 전달하는 데코레이터
def pass_spark_dataframe(func):
    def wrapper(*args):
        spark_df = make_spark_dataframe(*args)
        return func(spark_df)
    return wrapper

# spark 객체를 이용하여 file_path에 존재하는 데이터를 읽어와 sparkdataframe을 생성하는 함수수
def make_spark_dataframe(spark:object, file_path:str)->object:
    spark_df = spark.read() \
              .format("json") \
              .option("multiLine", True) \
              .load(file_path)
    print(f"{file_path} data를 load 합니다.")
    return spark_df

# RAWDATA를 정제하여 `USER` 테이블을 생성하는 함수
@pass_spark_dataframe
def make_user_dataframe(spark_df:object)->object:
    spark_df = spark_df(F.explode("ranking").alias())