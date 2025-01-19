from pyspark.sql import SparkSession
from datetime import datetime , timedelta
import spark_common

# spark job ui 확인을 위한 python file
def main():
    #spark = SparkSession.builder \
    #                    .master("local[2]") \
    #                    .appName("Spark_Submit") \
    #                    .config("spark.eventLog.enabled","true")\
    #                    .config("spark.eventLog.dir","/opt/spark-events")\
    #                    .config("spark.history.fs.logDirectory","/opt/spark-events")\
    #                    .config("spark.executor.memory","2G")\
    #                    .getOrCreate()

    spark = SparkSession.builder \
                        .master("spark://spark-master:7077") \
                        .appName("Spark_Submit") \
                        .config("spark.eventLog.enabled","true")\
                        .config("spark.eventLog.dir","/opt/spark-events")\
                        .config("spark.history.fs.logDirectory","/opt/spark-events")\
                        .config("spark.executor.cores","2")\
                        .getOrCreate()
    
    # batch일자의 data와 batch 전날 data를 load
    UTC = datetime.now()
    batch_date= UTC + timedelta(hours=9)
    batch_yesterday_date=batch_date - timedelta(days=1)
    
    batch_date= batch_date.strftime("%Y-%m-%d")
    batch_yesterday_date=batch_yesterday_date.strftime("%Y-%m-%d")

    batch_data_path= f"/opt/bitnami/spark/data/ranking_{batch_date}.json" # batch일 데이터 경로
    batch_y_data_path= f"/opt/bitnami/spark/data/ranking_{batch_yesterday_date}.json" # batch전날 데이터 경로
    exp_data_path= "/opt/bitnami/spark/data/maple_exp.csv"
    
    # BATCH일의 USER 테이블 생성
    user_batch_df= spark_common.make_user_dataframe(spark,batch_data_path)
    user_batch_df.show(10)

    # BATCH전날의 USER 테이블 생성
    user_yesterday_df=spark_common.make_user_dataframe(spark,batch_y_data_path)

    # Join된 Dataframe 생성성
    joined_df=spark_common.make_joined_dataframe(user_batch_df,user_yesterday_df)

    # LEVEL 테이블 생성 
    level_df=spark_common.make_exp_dataframe(spark,exp_data_path)
    level_df.show(10)

    # // 사용할 데이터 테이블 
    # [ClassStatus table]
    class_status_df = spark_common.TableBuilder(user_batch_df)
    class_status_df = class_status_df.agg_class_status()
    class_status_df.show(10)

    # [AchievementSummary table]
    achievement_summary_df = spark_common.TableBuilder(joined_df)
    achievement_summary_df = achievement_summary_df.agg_achive_summary()
    achievement_summary_df.show(10)
                        
    # [UserExp table]
    user_exp_agg_df = spark_common.TableBuilder(joined_df)
    user_exp_agg_df = user_exp_agg_df.agg_user_exp(level_df)
    user_exp_agg_df.show(10)

    # [ClassExp table]
    class_exp_df = spark_common.TableBuilder(user_exp_agg_df)
    class_exp_df = class_exp_df.agg_class_exp()
    class_exp_df.show(10)

if __name__ == "__main__":
    main()