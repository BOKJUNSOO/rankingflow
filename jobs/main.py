from pyspark.sql import SparkSession
from datetime import datetime , timedelta
from spark_common.base import make_user_dataframe, make_exp_dataframe , make_joined_dataframe
from spark_common.filter import RankingDataModel
from spark_common.save import ElasticSearch, MySQL
if __name__ == "__main__":

    spark = SparkSession.builder \
                        .master("local") \
                        .appName("Spark_Submit") \
                        .config("spark.jars","/opt/airflow/resources/elasticsearch-spark-30_2.12-8.11.1.jar,/opt/airflow/resources/mysql-connector-j-8.0.33.jar") \
                        .getOrCreate()

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

    # Join된 Dataframe 생성성
    joined_df=make_joined_dataframe(user_batch_df,user_yesterday_df)

    # LEVEL 테이블 생성 
    level_df=make_exp_dataframe(spark,exp_data_path)
    level_df.show(10)

    # // 사용할 데이터 테이블 
    # [ClassStatus table]
    class_status_df = RankingDataModel(user_batch_df)
    class_status_df = class_status_df.agg_class_status()
    class_status_df.show(10)

    # [AchievementSummary table]
    achievement_summary_df = RankingDataModel(joined_df)
    achievement_summary_df = achievement_summary_df.agg_achive_summary()
    achievement_summary_df.show(10)
                        
    # [UserExp table]
    user_exp_agg_df = RankingDataModel(joined_df)
    user_exp_agg_df = user_exp_agg_df.agg_user_exp(level_df)
    user_exp_agg_df.show(10)

    # [ClassExp table]
    class_exp_df = RankingDataModel(user_exp_agg_df)
    class_exp_df = class_exp_df.agg_class_exp()
    class_exp_df.show(10)

    # save_data to elasticSearch
    save_to_elastic_search=ElasticSearch("http://es:9200")
    save_to_elastic_search.write(class_status_df,f"class_status_{batch_date}")
    save_to_elastic_search.write(achievement_summary_df,f"achievement_summary_{batch_date}")
    save_to_elastic_search.write(user_exp_agg_df,f"user_exp_{batch_date}")
    save_to_elastic_search.write(class_exp_df,f"class_exp_{batch_date}")

    # save_data to MySQL
    save_to_mysql_db=MySQL("jdbc:mysql://localhost:3307/rankinginfo")
    save_to_mysql_db.write(class_status_df,f"class_status_df")
    save_to_mysql_db.write(achievement_summary_df,f"achievement_summary_df")
    save_to_mysql_db.write(user_exp_agg_df,f"user_exp_agg_df")
    save_to_mysql_db.write(class_exp_df,f"class_exp_df")
