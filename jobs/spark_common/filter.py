import pyspark.sql.functions as F

class DataFrameFilter():
    # USER 테이블로부터 Class_Status 테이블로 변환시키는 함수
    def agg_status(df):
        filtered_df = df.groupBy("class","date").pivot("status") \
                      .agg(F.count("status"))
        return filtered_df
    def agg_class_exp(df):
        pass
    def agg_user_exp(df):
        pass
def spark_filter():
    pass