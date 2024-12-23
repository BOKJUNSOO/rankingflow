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

    # USER 테이블 생성
    user_df=make_user_dataframe(spark,batch_data_path)
    user_df.show(10)

    # LEVEL 테이블 생성 
    level_df=make_exp_dataframe(spark,exp_data_path)
    level_df.show(10)

    # Class_Status 테이블 생성
    class_status = DataFrameFilter()
    class_status_df = class_status.agg_status(user_df)
    class_status_df.show(10)
                        

