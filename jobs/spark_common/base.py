import pyspark.sql.functions as F
from pyspark.sql.types import StructType, IntegerType,DoubleType, StructField

# 생성한 sparkdataframe을 정제해주는 함수(func)에 전달하는 데코레이터
def pass_spark_dataframe(func):
    def wrapper(spark, file_path):
        spark_df = read_spark(spark, file_path)
        return func(spark_df)
    return wrapper

# spark 객체를 이용하여 file_path에 존재하는 데이터를 읽어와 sparkdataframe을 생성하는 함수
def read_spark(spark:object, file_path:str)->object:
    if ".json" in file_path:
        spark_df = spark.read \
                    .format("json") \
                    .option("multiLine", True) \
                    .load(file_path)
        print(f"{file_path} data를 load 합니다.")
    else:
        schema = StructType([
            StructField("row_number",IntegerType(),True),
            StructField("level",IntegerType(),True),
            StructField("need_exp",DoubleType(), True)
        ])
        print("Level 테이블을 생성합니다.")
        spark_df = spark.read \
                        .format("csv") \
                        .schema(schema) \
                        .option("multiLine", True) \
                        .load(file_path)
    return spark_df

# maple_exp를 정제하여 `LEVEL` 테이블을 생성하는 함수 
@pass_spark_dataframe
def make_exp_dataframe(spark_df:object)->object:
    spark_df = spark_df.dropna()
    spark_df = spark_df.select("level","need_exp")
    return spark_df
        
# RAWDATA를 정제하여 `USER` 테이블을 생성하는 함수
@pass_spark_dataframe
def make_user_dataframe(spark_df:object)->object:
    spark_df = spark_df.select(F.explode("ranking").alias("USER"))
    spark_df = spark_df.select("USER.character_name",
                               "USER.date",
                               "USER.class_name",
                               "USER.sub_class_name",
                               F.col("USER.character_level").cast("integer").alias("character_level"),
                               "USER.character_exp",
                               F.col("USER.ranking").cast("integer").alias("ranking"))
    # sub_class와 class_name 중 하나를 사용한다.
    spark_df = spark_df.withColumn("class",spark_df["sub_class_name"])
    spark_df = spark_df.withColumn("class",F.when(spark_df["sub_class_name"]== "", spark_df["class_name"]) \
                                             .otherwise(spark_df["class"]))
    spark_df = spark_df.drop("class_name","sub_class_name")

    # 각 유저가 위치한 지역정보 컬럼 추가
    spark_df = spark_df.withColumn("status",
                       F.when(spark_df["character_level"]>=290,"Tallahart") \
                        .when((spark_df["character_level"]<=289)&(spark_df["character_level"]>=285),"Carcion") \
                        .when((spark_df["character_level"]<=284)&(spark_df["character_level"]>=280),"Arteria") \
                        .when((spark_df["character_level"]<=279)&(spark_df["character_level"]>=275),"Dowonkyung") \
                        .when((spark_df["character_level"]<=274)&(spark_df["character_level"]>=270),"Odium") \
                        .when((spark_df["character_level"]<=269)&(spark_df["character_level"]>=265),"HotelArcs") \
                        .when((spark_df["character_level"]<=264)&(spark_df["character_level"]>=260),"Cernium") \
                        .otherwise("AcaneRiver"))
    return spark_df

# BATCH 일과 전날에 모두 존재하는 character_name을 기준으로 JOIN하고 정제하는 함수
def make_joined_dataframe(batch_df:object,yesterday_df:object)->object:
    joined_df = batch_df.join(yesterday_df,batch_df["character_name"] ==  yesterday_df["character_name"],how ="inner")
    joined_df = joined_df.select(
        batch_df["character_name"],
        batch_df["date"],
        batch_df["class"],
        batch_df["character_level"].alias("character_level_today"),
        yesterday_df["character_level"].alias("charcter_level_yesterday"),
        batch_df["character_exp"].alias("character_exp_today"),
        yesterday_df["character_exp"].alias("character_exp_yesterday"),
        batch_df["status"].alias("status_today"),
        yesterday_df["status"].alias("status_yesterday")
    )
    return joined_df
