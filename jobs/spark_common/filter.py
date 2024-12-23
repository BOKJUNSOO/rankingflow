import pyspark.sql.functions as F

class DataFrameFilter():
    # USER 테이블로부터 Class_Status 테이블을 만드는 함수
    def agg_class_status(self,df):
        filtered_df = df.groupBy("class","date").pivot("status") \
                      .agg(F.count("status"))
        return filtered_df
    
    # BATCH 전날과 BATCH 일의 데이터를 이용해서 AchievementSummary 테이블을 만드는 함수
    def agg_achive_summary(joined_df):
        pass

    # BATCH 전날과 BATCH 일의 데이터를 이용해서 user_exp_aggregate 테이블을 만드는 함수
    def agg_user_exp(self,joined_df,exp_df):
        pass
    
    # agg_user_exp의 리턴된 테이블로부터 class_exp_aggregate 테이블을 만드는 함수
    def agg_class_exp(df):
        pass
    
    

def spark_filter():
    pass