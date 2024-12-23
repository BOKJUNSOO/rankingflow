from pyspark.sql import SparkSession
from datetime import datetime , timedelta
from spark_common.base import make_user_dataframe, make_exp_dataframe
from spark_common.filter import DataFrameFilter
if __name__ == "__main__":

    spark = SparkSession.builder \
                        .master("local") \
                        .appName("Spark_Submit") \
                        .getOrCreate()
                        #.config()
    # batch일자의 data와 batch 전날 data를 load
    UTC = datetime.now()
    batch_date= UTC + timedelta(hours=9)
    batch_yesterday_date=batch_date - timedelta(days=1)
    
    batch_date= batch_date.strftime("%Y-%m-%d")
    batch_yesterday_date=batch_yesterday_date.strftime("%Y-%m-%d")

    batch_data_path= f"/opt/airflow/data/ranking_{batch_date}.json" # batch일 데이터 경로
    batch_y_data_path= f"/opt/airflow/data/ranking_{batch_yesterday_date}.json" # batch전날 데이터 경로
    exp_data_path= "/opt/airflow/data/maple_exp.csv"

    # BATCH일의 USER 테이블 생성
    user_batch_df=make_user_dataframe(spark,batch_data_path)
    user_batch_df.show(10)

    # BATCH전날의 USER 테이블 생성
    user_yesterday_df=make_user_dataframe(spark,batch_y_data_path)

    # LEVEL 테이블 생성 
    level_df=make_exp_dataframe(spark,exp_data_path)
    level_df.show(10)
    
    # 저장될 데이터 모델
    make_dataframe = DataFrameFilter()
    # ClassStatus table
    class_status_df = make_dataframe.agg_class_status(user_batch_df)
    class_status_df.show(10)

    # AchievementSummary
    achievement_summary_df = make_dataframe.agg_achive_summary(user_batch_df)
    achievement_summary_df.show(10)
                        
    # UserExp table
    user_exp_agg_df = make_dataframe.agg_user_exp(user_batch_df,user_yesterday_df,level_df)
    user_exp_agg_df.show(10)

    # ClassExp table
    class_exp_df = make_dataframe.agg_class_exp(user_exp_agg_df)
    class_exp_df.show(10)
